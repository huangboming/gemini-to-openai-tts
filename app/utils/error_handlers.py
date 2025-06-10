from typing import Any


class ServiceException(Exception):
    """Base class for service-related exceptions."""

    def __init__(self, status_code: int, detail: dict[str, Any]):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail.get("message", "Service error occurred"))


class UpstreamAPIException(ServiceException):
    """Exception for upstream Gemini API related errors."""


class AudioProcessingException(ServiceException):
    """Exception for errors during audio transcoding."""
