"""Shared fixtures for all WarEra client tests."""

from __future__ import annotations

import httpx
import pytest
import respx

from warera import AsyncWarEraClient, WarEraClient

BASE_URL = "https://api2.warera.io/trpc"


# ── Sync client fixtures ─────────────────────────────────────────────────────


@pytest.fixture()
def mock_api() -> respx.MockRouter:
    """Return a ``respx`` router pre-configured for the API base URL."""
    with respx.mock(base_url=BASE_URL, assert_all_called=False) as router:
        yield router


@pytest.fixture()
def client() -> WarEraClient:
    """Return a sync :class:`WarEraClient` that closes after the test."""
    c = WarEraClient()
    yield c
    c.close()


# ── Async client fixtures ────────────────────────────────────────────────────


@pytest.fixture()
def async_client() -> AsyncWarEraClient:
    """Return an async :class:`AsyncWarEraClient` that closes after the test."""
    return AsyncWarEraClient()
