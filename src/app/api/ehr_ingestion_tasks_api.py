from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends

from app.api.api_response_models import CreatedResourceResponse
from app.api.dependencies import get_ehr_contexts_service
from app.domain.ehr_ingestion.ehr_contexts_service import EHRContextsService
from app.domain.ehr_ingestion.ehr_models import ElectronicPatientRecord

router = APIRouter()


@router.post(
    status_code=HTTPStatus.CREATED, path="", response_model=CreatedResourceResponse
)
async def create_ehr_ingestion_task(
    ehr: ElectronicPatientRecord,
    ehr_contexts_service: EHRContextsService = Depends(get_ehr_contexts_service),
) -> CreatedResourceResponse:
    # Mocking a task id, this could eventually run as a background task, right now I will just generate a UUID
    task_id = uuid4()

    await ehr_contexts_service.ingest_ehr(ehr=ehr)

    return CreatedResourceResponse(id=task_id)
