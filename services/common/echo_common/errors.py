from contextlib import asynccontextmanager

import httpx

from echo_common.http import (
    HTTP_ERR_INTERNAL,
    HTTP_ERR_RATE_LIMIT,
    HTTP_ERR_UNAUTHORIZED,
)


class ServiceError(Exception):
    """Base domain error carrying a stable code and a human-readable message."""

    code = "internal_error"
    message = "Something went wrong."
    http_status = HTTP_ERR_INTERNAL

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)


class TtsAuthError(ServiceError):
    code = "tts_auth"
    http_status = 502
    message = "TTS auth failed, check tts.api_key in private/config.yaml"


class TtsUnavailable(ServiceError):
    code = "tts_unavailable"
    http_status = 502
    message = "Voice service is unavailable."


class LlmError(ServiceError):
    code = "llm_error"
    http_status = 502
    message = "Language model request failed."


class LlmRateLimited(LlmError):
    code = "llm_rate_limited"
    http_status = 429
    message = "Rate limited. Wait a minute or switch to Ollama."


class SttError(ServiceError):
    code = "stt_error"
    http_status = 502
    message = "Speech-to-text failed."


def to_payload(exc):
    """Shape a domain error into the wire vocabulary clients consume."""
    return {"code": exc.code, "message": exc.message}


def as_service_error(exc):
    """Pass through domain errors, wrap anything unexpected as generic."""
    return exc if isinstance(exc, ServiceError) else ServiceError()


# each service gets its own error types used when mapping an upstream failure
_AUTH = {"tts": TtsAuthError}
_UNAVAILABLE = {
    "tts": TtsUnavailable,
    "llm": LlmError,
    "stt": SttError,
}


def from_upstream(service, exc):
    """Map an upstream httpx failure to the right domain error."""
    unavailable = _UNAVAILABLE.get(service, ServiceError)

    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        if status == HTTP_ERR_UNAUTHORIZED:
            return _AUTH.get(service, unavailable)()
        if status == HTTP_ERR_RATE_LIMIT:
            return LlmRateLimited()
        return unavailable()

    # timeouts, connection refused and other transport errors
    return unavailable()


@asynccontextmanager
async def upstream(service):
    """Wrap an httpx call block, converting transport errors to domain errors."""
    try:
        yield
    except ServiceError:
        raise
    except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError) as e:
        raise from_upstream(service, e) from e
