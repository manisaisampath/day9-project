import httpx
import pytest

from day_9_project.client import AsyncAPIClient


@pytest.fixture
def mock_client():
    def handler(request):
        return httpx.Response(
            200,
            json={"message": "Success"},
        )

    transport = httpx.MockTransport(handler)
    client = AsyncAPIClient()
    client.client = httpx.AsyncClient(
        transport=transport,
        base_url="https://test.example.com",
        timeout=10,
    )
    return client


@pytest.mark.asyncio
async def test_successful_get(mock_client):
    result = await mock_client.get("/test")
    assert result == {"message": "Success"}
    await mock_client.close()


@pytest.mark.asyncio
async def test_http_error():
    def handler(request):
        return httpx.Response(404)

    client = AsyncAPIClient()
    client.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://test.example.com",
    )

    with pytest.raises(httpx.HTTPStatusError):
        await client.get("/missing")

    await client.close()


@pytest.mark.asyncio
async def test_retry_on_server_error():
    attempts = 0

    def handler(request):
        nonlocal attempts
        attempts += 1

        if attempts < 2:
            return httpx.Response(503)

        return httpx.Response(200, json={"status": "recovered"})

    client = AsyncAPIClient()
    client.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://test.example.com",
    )

    result = await client.get("/retry")
    assert result == {"status": "recovered"}
    await client.close()


@pytest.mark.asyncio
async def test_timeout_error():
    def handler(request):
        raise httpx.ReadTimeout("Request timed out")

    client = AsyncAPIClient()
    client.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://test.example.com",
    )

    with pytest.raises(httpx.ReadTimeout):
        await client.get("/timeout")

    await client.close()


@pytest.mark.asyncio
async def test_authentication_header():
    def handler(request):
        assert request.headers["Authorization"] == "Bearer my_test_key"
        return httpx.Response(200, json={"authenticated": True})

    client = AsyncAPIClient()
    client.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://test.example.com",
        headers={"Authorization": "Bearer my_test_key"},
    )

    result = await client.get("/auth")
    assert result == {"authenticated": True}
    await client.close()


@pytest.mark.asyncio
async def test_request_endpoint():
    def handler(request):
        assert request.url.path == "/users"
        return httpx.Response(200, json={"users": []})

    client = AsyncAPIClient()
    client.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://test.example.com",
    )

    result = await client.get("/users")
    assert result == {"users": []}
    await client.close()


@pytest.mark.asyncio
async def test_client_close():
    client = AsyncAPIClient()
    await client.close()
    assert client.client.is_closed


@pytest.mark.asyncio
async def test_context_manager():
    client = AsyncAPIClient()

    async with client as api:
        assert api is client
        assert not api.client.is_closed

    assert client.client.is_closed
