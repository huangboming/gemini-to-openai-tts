from google import genai
from google.api_core import exceptions as google_exceptions
from google.api_core.exceptions import (
    InternalServerError,
    InvalidArgument,
    PermissionDenied,
    ServiceUnavailable,
)
from google.genai import types

from app.core.config import settings
from app.core.logging import get_logger
from app.models.schemas import SpeechRequest
from app.utils.error_handlers import UpstreamAPIException


# 初始化日志器
logger = get_logger(__name__)


class GeminiClient:
    """
    封装了与 Google Gemini API 进行文本转语音交互的客户端。
    """

    def __init__(self):
        """
        初始化 Gemini 客户端，通过 API 密钥进行配置，并准备 TTS 模型。
        """
        logger.debug("Initializing Gemini client")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = "gemini-2.5-flash-preview-tts"
        logger.debug("Gemini client initialized with model: %s", self.model)

    def _construct_prompt(self, request: SpeechRequest) -> str:
        """
        根据技术规约 3.3 节的要求，从 SpeechRequest 对象构造 prompt。

        此方法将 `instructions` 和非默认的 `speed` 参数合并到
        一个单独的文本 prompt 中，以指导 TTS 模型的发音。

        Args:
            request: 包含输入文本、语速和指示的 SpeechRequest 对象。

        Returns:
            为 Gemini API 调用构造的完整 prompt 字符串。
        """
        prompt_parts = []

        # 根据规约，如果提供了 `instructions`，则将其添加到 prompt 的开头。
        if request.instructions:
            prompt_parts.append(request.instructions)

        # 根据规约，如果 `speed` 不是默认值 1.0，则添加语速指令。
        # 我们使用自然语言指令来表达语速要求。
        if request.speed and request.speed != 1.0:
            if request.speed < 1.0:
                prompt_parts.append(
                    f"请以较慢的语速朗读，大约是正常语速的 {request.speed} 倍。"
                )
            else:
                prompt_parts.append(
                    f"请以较快的语速朗读，大约是正常语速的 {request.speed} 倍。"
                )

        # 最后，添加核心的输入文本。
        prompt_parts.append(request.input)

        final_prompt = "\n\n".join(prompt_parts)
        logger.debug(
            "Constructed prompt for TTS",
            extra={
                "prompt_length": len(final_prompt),
                "has_speed_instruction": bool(request.speed and request.speed != 1.0),
                "has_custom_instructions": bool(request.instructions),
            },
        )
        return final_prompt

    def _get_voice_config(self, voice_name: str) -> types.VoiceConfig:
        """
        根据语音名称创建语音配置对象。

        Args:
            voice_name: 语音名称，应该是 VALID_VOICES 中的一个。

        Returns:
            配置好的 VoiceConfig 对象。
        """
        return types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name=voice_name,
            )
        )

    def generate_audio(self, request: SpeechRequest) -> str:
        """
        使用 Gemini TTS API 从文本生成音频。

        此方法会构造一个 prompt，调用 Gemini API，并处理响应以提取
        音频数据。

        Args:
            request: 包含生成语音所需全部信息的 SpeechRequest 对象。

        Returns:
            表示生成音频的 base64 编码字符串。

        Raises:
            UpstreamAPIException: 如果 Gemini API 调用失败或返回可处理的错误。
        """
        prompt = self._construct_prompt(request)
        voice_config = self._get_voice_config(request.voice)

        logger.info(
            "Generating audio via Gemini API",
            extra={
                "model": self.model,
                "voice": request.voice,
                "prompt_preview": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            },
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(voice_config=voice_config),
                ),
            )

            # 提取音频数据（base64 编码的字符串）
            audio_data = response.candidates[0].content.parts[0].inline_data.data

            logger.info(
                "Successfully generated audio from Gemini API",
                extra={"audio_data_length": len(audio_data), "voice": request.voice},
            )

            return audio_data

        except PermissionDenied as e:
            # API Key 无效或权限不足
            logger.error(
                "Gemini API authentication failed",
                extra={"error": str(e)},
                exc_info=True,
            )
            raise UpstreamAPIException(
                status_code=500,
                detail={
                    "type": "api_error",
                    "message": "Upstream API authentication failed. Check server configuration.",
                },
            ) from e
        except InvalidArgument as e:
            # 输入文本可能被内容策略阻止
            logger.warning(
                "Gemini API rejected request due to content policy",
                extra={
                    "error": str(e),
                    "voice": request.voice,
                    "input_preview": request.input[:50] + "..."
                    if len(request.input) > 50
                    else request.input,
                },
            )
            raise UpstreamAPIException(
                status_code=400,
                detail={
                    "type": "invalid_request_error",
                    "message": "The input text was blocked by the upstream content safety policy.",
                },
            ) from e
        except (ServiceUnavailable, InternalServerError) as e:
            # Gemini 服务暂时不可用或内部错误
            logger.error(
                "Gemini API service unavailable",
                extra={"error": str(e), "error_type": type(e).__name__},
                exc_info=True,
            )
            raise UpstreamAPIException(
                status_code=502,
                detail={
                    "type": "api_error",
                    "message": "The upstream API (Gemini) is currently unavailable.",
                },
            ) from e
        except google_exceptions.GoogleAPICallError as e:
            # 其他未指定的 Google API 错误
            logger.error(
                "Unexpected Gemini API error",
                extra={"error": str(e), "error_type": type(e).__name__},
                exc_info=True,
            )
            raise UpstreamAPIException(
                status_code=500,
                detail={
                    "type": "api_error",
                    "message": f"An unexpected upstream API error occurred: {e}",
                },
            ) from e
