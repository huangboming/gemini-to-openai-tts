from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import verify_api_key
from app.models.schemas import (
    AVAILABLE_MODELS,
    VOICE_LIST,
    ErrorDetail,
    ErrorResponse,
    ModelInfo,
    ModelsResponse,
    SpeechRequest,
    VoicesResponse,
)
from app.services.audio_processor import AudioProcessor
from app.services.gemini_client import GeminiClient
from app.utils.error_handlers import ServiceException


# 初始化日志器
logger = get_logger(__name__)

app = FastAPI(
    title="Gemini to OpenAI TTS Proxy",
    description="A proxy service to convert OpenAI TTS API calls to Gemini TTS API",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info(
        "Gemini to OpenAI TTS Proxy starting up",
        extra={"version": "0.1.0", "log_level": settings.LOG_LEVEL},
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "gemini-to-openai-tts"}


@app.get("/v1/audio/models", response_model=ModelsResponse)
async def get_audio_models():
    """
    Get list of available audio models.
    
    Returns a list of models compatible with OpenAI TTS API format.
    """
    logger.info("Models list requested")
    models = [ModelInfo(**model) for model in AVAILABLE_MODELS]
    return ModelsResponse(data=models)


@app.get("/v1/audio/voices", response_model=VoicesResponse)
async def get_audio_voices():
    """
    Get list of available voice IDs.
    
    Returns a list of voice IDs compatible with Open WebUI format.
    """
    logger.info("Voices list requested")
    return VoicesResponse(voices=VOICE_LIST)


@app.exception_handler(ServiceException)
async def service_exception_handler(request: Request, exc: ServiceException):
    """Handles custom service exceptions."""
    logger.warning(
        "Service exception occurred: %s",
        exc.detail,
        extra={
            "status_code": exc.status_code,
            "endpoint": str(request.url),
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(
                message=exc.detail.get("message", "An error occurred"),
                type=exc.detail.get("type", "api_error"),
                param=exc.detail.get("param"),
                code=exc.detail.get("code"),
            )
        ).model_dump(exclude_none=True),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handles Pydantic validation errors."""
    first_error = exc.errors()[0]
    param = ".".join(str(loc) for loc in first_error["loc"])

    logger.info(
        "Request validation failed: %s",
        first_error["msg"],
        extra={
            "param": param,
            "endpoint": str(request.url),
            "method": request.method,
            "errors": exc.errors(),
        },
    )

    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error=ErrorDetail(
                message=first_error["msg"],
                type="invalid_request_error",
                param=param,
            )
        ).model_dump(exclude_none=True),
    )


@app.post(
    "/v1/audio/speech",
    response_model=None,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
    },
    dependencies=[Depends(verify_api_key)],
)
def text_to_speech(request: SpeechRequest):
    """
    Converts text to speech.
    """
    logger.info(
        "TTS request received",
        extra={
            "model": request.model,
            "voice": request.voice,
            "response_format": request.response_format,
            "speed": request.speed,
            "input_length": len(request.input),
            "has_instructions": bool(request.instructions),
        },
    )

    content_type_map = {
        "mp3": "audio/mpeg",
        "opus": "audio/opus",
        "aac": "audio/aac",
        "flac": "audio/flac",
        "wav": "audio/wav",
        "pcm": "audio/l16; rate=24000; channels=1",
    }

    try:
        gemini_client = GeminiClient()

        logger.debug("Generating audio via Gemini API")
        raw_audio = gemini_client.generate_audio(request)

        logger.debug("Transcoding audio to format: %s", request.response_format)
        transcoded_audio = AudioProcessor.transcode_audio(
            raw_audio, request.response_format
        )

        media_type = content_type_map.get(
            request.response_format, "application/octet-stream"
        )

        logger.info(
            "TTS request completed successfully",
            extra={
                "response_format": request.response_format,
                "output_size_bytes": len(transcoded_audio),
            },
        )

        return Response(content=transcoded_audio, media_type=media_type)

    except Exception as e:
        logger.error(
            "TTS request failed: %s",
            str(e),
            extra={
                "model": request.model,
                "voice": request.voice,
                "response_format": request.response_format,
            },
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail="An internal server error occurred."
        ) from e
