"""Exceptions raised by the WarEra API client."""

from __future__ import annotations


class WarEraError(Exception):
    """Base exception for all WarEra client errors."""


class WarEraAPIError(WarEraError):
    """Raised when the API returns a non-success HTTP status code."""

    def __init__(self, status_code: int, detail: str | None = None) -> None:
        self.status_code = status_code
        self.detail = detail
        message = f"API request failed with status {status_code}"
        if detail:
            message += f": {detail}"
        super().__init__(message)


class WarEraConnectionError(WarEraError):
    """Raised when the client cannot reach the API."""
