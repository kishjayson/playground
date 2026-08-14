from __future__ import annotations

import base64
import copy
import os
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://a.simplemdm.com/api/v1"
DEVICE_SECRET_FIELDS = {
    "filevault_recovery_key",
    "firmware_password",
    "recovery_lock_password",
}


class SimpleMDMClient:
    """Thin asynchronous client for SimpleMDM GET endpoints."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.api_key = api_key or os.environ["SIMPLEMDM_API_KEY"]
        self.base_url = (base_url or os.getenv("SIMPLEMDM_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            auth=(self.api_key, ""),
            timeout=timeout,
            transport=transport,
        )

    async def __aenter__(self) -> "SimpleMDMClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._client.aclose()

    @staticmethod
    def _params(params: dict[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in params.items() if value not in (None, "", 0)}

    @staticmethod
    def redact_device_secrets(payload: dict[str, Any]) -> dict[str, Any]:
        result = copy.deepcopy(payload)

        def walk(value: Any) -> None:
            if isinstance(value, dict):
                for key in list(value):
                    if key in DEVICE_SECRET_FIELDS:
                        value.pop(key)
                    else:
                        walk(value[key])
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(result)
        return result

    async def get(self, path: str, *, redact_device_secrets: bool = False, **params: Any) -> dict[str, Any]:
        response = await self._client.get(path, params=self._params(params))
        response.raise_for_status()
        payload = response.json()
        if redact_device_secrets:
            return self.redact_device_secrets(payload)
        return payload

    async def get_content(self, path: str, **params: Any) -> dict[str, str]:
        response = await self._client.get(path, params=self._params(params))
        response.raise_for_status()
        content_type = response.headers.get("content-type", "application/octet-stream")

        if content_type.startswith("text/") or "json" in content_type or "xml" in content_type:
            return {"content_type": content_type, "content": response.text}

        return {
            "content_type": content_type,
            "content_base64": base64.b64encode(response.content).decode("ascii"),
        }
