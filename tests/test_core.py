"""Tests for helper functions and client lifecycle."""

from __future__ import annotations

import httpx
import pytest
import respx

from warera import WarEraClient, AsyncWarEraClient
from warera.client import _strip_nones, _handle_response, _DEFAULT_BASE_URL
from warera.exceptions import WarEraAPIError, WarEraConnectionError, WarEraError


# ═════════════════════════════════════════════════════════════════════════════
#  _strip_nones
# ═════════════════════════════════════════════════════════════════════════════


class TestStripNones:
    def test_removes_none_values(self):
        assert _strip_nones({"a": 1, "b": None, "c": "x"}) == {"a": 1, "c": "x"}

    def test_all_none(self):
        assert _strip_nones({"a": None, "b": None}) == {}

    def test_no_nones(self):
        data = {"a": 1, "b": 2}
        assert _strip_nones(data) == data

    def test_empty_dict(self):
        assert _strip_nones({}) == {}

    def test_preserves_falsy_non_none(self):
        """0, empty string, False are kept — only None is removed."""
        assert _strip_nones({"a": 0, "b": "", "c": False, "d": None}) == {
            "a": 0,
            "b": "",
            "c": False,
        }


# ═════════════════════════════════════════════════════════════════════════════
#  _handle_response
# ═════════════════════════════════════════════════════════════════════════════


class TestHandleResponse:
    def test_returns_json_on_200(self):
        resp = httpx.Response(200, json={"result": "ok"})
        assert _handle_response(resp) == {"result": "ok"}

    def test_raises_api_error_on_non_200(self):
        resp = httpx.Response(500, text="Internal Server Error")
        with pytest.raises(WarEraAPIError) as exc_info:
            _handle_response(resp)
        assert exc_info.value.status_code == 500
        assert "Internal Server Error" in exc_info.value.detail

    def test_raises_api_error_on_404(self):
        resp = httpx.Response(404, text="Not Found")
        with pytest.raises(WarEraAPIError) as exc_info:
            _handle_response(resp)
        assert exc_info.value.status_code == 404

    def test_raises_api_error_on_422(self):
        resp = httpx.Response(422, json={"error": "validation failed"})
        with pytest.raises(WarEraAPIError) as exc_info:
            _handle_response(resp)
        assert exc_info.value.status_code == 422


# ═════════════════════════════════════════════════════════════════════════════
#  Exception hierarchy
# ═════════════════════════════════════════════════════════════════════════════


class TestExceptions:
    def test_api_error_is_warera_error(self):
        assert issubclass(WarEraAPIError, WarEraError)

    def test_connection_error_is_warera_error(self):
        assert issubclass(WarEraConnectionError, WarEraError)

    def test_api_error_message_without_detail(self):
        err = WarEraAPIError(503)
        assert "503" in str(err)
        assert err.detail is None

    def test_api_error_message_with_detail(self):
        err = WarEraAPIError(400, "bad request body")
        assert "400" in str(err)
        assert "bad request body" in str(err)
        assert err.detail == "bad request body"


# ═════════════════════════════════════════════════════════════════════════════
#  Client lifecycle & configuration
# ═════════════════════════════════════════════════════════════════════════════


class TestClientLifecycle:
    def test_default_base_url(self):
        c = WarEraClient()
        assert c._base_url == _DEFAULT_BASE_URL
        c.close()

    def test_custom_base_url(self):
        c = WarEraClient(base_url="https://custom.example.com/trpc/")
        assert c._base_url == "https://custom.example.com/trpc"
        c.close()

    def test_api_key_sets_header(self):
        c = WarEraClient("my-secret-key")
        assert c._client.headers["X-API-Key"] == "my-secret-key"
        c.close()

    def test_no_api_key_omits_header(self):
        c = WarEraClient()
        assert "X-API-Key" not in c._client.headers
        c.close()

    def test_api_key_sent_in_request(self, mock_api):
        """The X-API-Key header is sent with every request."""
        mock_api.post("/country.getAllCountries").mock(
            return_value=httpx.Response(200, json={"result": "ok"})
        )
        c = WarEraClient("test-key-123")
        c.get_all_countries()
        request = mock_api.calls[0].request
        assert request.headers["X-API-Key"] == "test-key-123"
        c.close()

    def test_context_manager(self):
        with WarEraClient() as c:
            assert isinstance(c, WarEraClient)
        # after exiting, client should be closed (no assertion needed — just
        # verifying no exception is raised)

    def test_connection_error_raised(self, mock_api, client):
        """When the server is unreachable, WarEraConnectionError is raised."""
        mock_api.post("/country.getAllCountries").mock(
            side_effect=httpx.ConnectError("connection refused")
        )
        with pytest.raises(WarEraConnectionError):
            client.get_all_countries()

    def test_api_error_raised_on_500(self, mock_api, client):
        mock_api.post("/country.getAllCountries").mock(
            return_value=httpx.Response(500, text="boom")
        )
        with pytest.raises(WarEraAPIError) as exc_info:
            client.get_all_countries()
        assert exc_info.value.status_code == 500


class TestAsyncClientLifecycle:
    def test_default_base_url(self):
        c = AsyncWarEraClient()
        assert c._base_url == _DEFAULT_BASE_URL

    def test_custom_base_url(self):
        c = AsyncWarEraClient(base_url="https://other.example.com/trpc/")
        assert c._base_url == "https://other.example.com/trpc"

    def test_api_key_sets_header(self):
        c = AsyncWarEraClient("async-secret")
        assert c._client.headers["X-API-Key"] == "async-secret"

    def test_no_api_key_omits_header(self):
        c = AsyncWarEraClient()
        assert "X-API-Key" not in c._client.headers

    @pytest.mark.asyncio
    async def test_api_key_sent_in_request(self, mock_api):
        """The X-API-Key header is sent with every async request."""
        mock_api.post("/country.getAllCountries").mock(
            return_value=httpx.Response(200, json={"result": "ok"})
        )
        async with AsyncWarEraClient("async-key-456") as c:
            await c.get_all_countries()
        request = mock_api.calls[0].request
        assert request.headers["X-API-Key"] == "async-key-456"

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        async with AsyncWarEraClient() as c:
            assert isinstance(c, AsyncWarEraClient)
