from http import HTTPStatus
from typing import Any

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_ehr_ingestion_task(client: AsyncClient) -> None:
    request_payload: dict[str, Any] = {}
    response = await client.post("/api/ehr-ingestion-tasks", json=request_payload)
    assert response.status_code == HTTPStatus.CREATED
    response_payload = response.json()
    assert response_payload["id"]
