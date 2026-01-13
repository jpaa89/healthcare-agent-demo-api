from http import HTTPStatus
from typing import Any
from uuid import uuid4

from fastapi import APIRouter

router = APIRouter()


@router.post(status_code=HTTPStatus.CREATED, path="")
async def create_ehr_ingestion_task(ehr_data: dict[str, Any]) -> dict[str, str]:
    # Mocking a task id
    task_id = uuid4()

    return {"id": str(task_id)}
