from typing import Literal

from pydantic import BaseModel, Field


# 根据 spec.md 文档附录 A，这是 Gemini 支持的有效语音名称。
VALID_VOICES = Literal[
    "Zephyr",
    "Puck",
    "Charon",
    "Kore",
    "Fenrir",
    "Leda",
    "Orus",
    "Aoede",
    "Callirrhoe",
    "Autonoe",
    "Enceladus",
    "Iapetus",
    "Umbriel",
    "Algieba",
    "Despina",
    "Erinome",
    "Algenib",
    "Rasalgethi",
    "Laomedeia",
    "Achernar",
    "Alnilam",
    "Schedar",
    "Gacrux",
    "Pulcherrima",
    "Achird",
    "Zubenelgenubi",
    "Vindemiatrix",
    "Sadachbia",
    "Sadaltager",
    "Sulafat",
]

# 提取语音列表以便在其他地方使用
VOICE_LIST = [
    "Zephyr",
    "Puck",
    "Charon",
    "Kore",
    "Fenrir",
    "Leda",
    "Orus",
    "Aoede",
    "Callirrhoe",
    "Autonoe",
    "Enceladus",
    "Iapetus",
    "Umbriel",
    "Algieba",
    "Despina",
    "Erinome",
    "Algenib",
    "Rasalgethi",
    "Laomedeia",
    "Achernar",
    "Alnilam",
    "Schedar",
    "Gacrux",
    "Pulcherrima",
    "Achird",
    "Zubenelgenubi",
    "Vindemiatrix",
    "Sadachbia",
    "Sadaltager",
    "Sulafat",
]

VALID_RESPONSE_FORMATS = Literal["mp3", "opus", "aac", "flac", "wav"]

# 支持的模型列表
AVAILABLE_MODELS = [
    {"id": "gemini-2.5-flash-preview-tts", "name": "Gemini 2.5 Flash TTS"}
]


class SpeechRequest(BaseModel):
    """
    用于验证 /v1/audio/speech 端点请求体的 Pydantic 模型。
    """

    model: str
    input: str
    voice: VALID_VOICES
    instructions: str | None = None
    speed: float | None = Field(default=1.0, ge=0.25, le=4.0)
    response_format: VALID_RESPONSE_FORMATS | None = "mp3"


class ErrorDetail(BaseModel):
    """
    标准错误响应中错误详情对象的 Pydantic 模型。
    """

    message: str
    type: str
    param: str | None = None
    code: str | None = None


class ErrorResponse(BaseModel):
    """
    标准错误响应的 Pydantic 模型。
    """

    error: ErrorDetail


class ModelInfo(BaseModel):
    """
    模型信息的 Pydantic 模型。
    """

    id: str
    name: str


class ModelsResponse(BaseModel):
    """
    模型列表响应的 Pydantic 模型。
    """

    data: list[ModelInfo]


class VoicesResponse(BaseModel):
    """
    语音列表响应的 Pydantic 模型。
    """

    voices: list[str]
