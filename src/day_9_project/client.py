import asyncio
from typing import Any

import httpx

from day_9_project.config import settings


class AsyncAPIClient:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient(
            base_url=settings.api_base_url,
            timeout=settings.request_timeout,
            headers={"Authorization": f"Bearer {settings.api_key}"},
        )

    async def get(self, endpoint: str) -> dict[str, Any]:
        for attempt in range(settings.max_retries + 1):
            try:
                response = await self.client.get(endpoint)

                if response.status_code in (500, 502, 503, 504):
                    response.raise_for_status()

                response.raise_for_status()
                return response.json()

            except (
                httpx.TimeoutException,
                httpx.TransportError,
                httpx.HTTPStatusError,
            ) as error:
                if isinstance(error, httpx.HTTPStatusError):
                    if error.response.status_code not in (500, 502, 503, 504):
                        raise

                if attempt == settings.max_retries:
                    raise

                await asyncio.sleep(2**attempt)

        raise RuntimeError("Request failed")

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> "AsyncAPIClient":
        return self

    async def __aexit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:
        await self.close()
