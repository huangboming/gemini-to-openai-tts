import base64
import io

from pydub import AudioSegment

from app.core.logging import get_logger
from app.utils.error_handlers import AudioProcessingException


# 初始化日志器
logger = get_logger(__name__)


class AudioProcessor:
    @staticmethod
    def transcode_audio(raw_audio_data: str, target_format: str) -> bytes:
        """
        Transcodes raw PCM audio data to the specified target format.

        Args:
            raw_audio_data: The raw PCM audio data from Gemini API (base64 encoded).
            target_format: The target audio format (e.g., 'mp3', 'wav').

        Returns:
            The transcoded audio data as bytes.

        Raises:
            AudioProcessingException: If an error occurs during audio processing.
        """
        logger.debug(
            "Starting audio transcoding",
            extra={
                "target_format": target_format,
                "input_data_length": len(raw_audio_data)
                if isinstance(raw_audio_data, str)
                else len(raw_audio_data),
            },
        )

        try:
            # Decode base64 audio data from Gemini API
            if isinstance(raw_audio_data, str):
                # If it's a string, decode from base64
                decoded_audio = base64.b64decode(raw_audio_data)
            else:
                # If it's already bytes, assume it's already decoded
                decoded_audio = raw_audio_data

            # Load raw PCM data with specified parameters
            # According to Gemini API docs, the audio is 24kHz, 16-bit, mono PCM
            audio_segment = AudioSegment.from_raw(
                io.BytesIO(decoded_audio),
                sample_width=2,  # 16-bit
                frame_rate=24000,  # 24kHz
                channels=1,  # Mono
            )

            # Export to the target format in-memory
            buffer = io.BytesIO()
            audio_segment.export(buffer, format=target_format)

            # Get the bytes value from the buffer
            buffer.seek(0)
            transcoded_data = buffer.read()

            logger.debug(
                "Audio transcoding completed successfully",
                extra={
                    "target_format": target_format,
                    "output_size_bytes": len(transcoded_data),
                },
            )

            return transcoded_data
        except Exception as e:
            logger.error(
                "Audio transcoding failed",
                extra={
                    "target_format": target_format,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
                exc_info=True,
            )
            raise AudioProcessingException(
                status_code=500,
                detail={
                    "type": "api_error",
                    "message": f"Internal server error during audio processing: {str(e)}",
                },
            ) from e
