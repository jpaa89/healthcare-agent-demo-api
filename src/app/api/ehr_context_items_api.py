from http import HTTPStatus

from fastapi import APIRouter, Depends

from app.api.api_response_models import ListedResourcesResponse
from app.api.dependencies import get_ehr_contexts_service
from app.domain.ehr_ingestion.ehr_context_models import EHRContextItem
from app.domain.ehr_ingestion.ehr_contexts_service import EHRContextsService

router = APIRouter()


@router.get(
    status_code=HTTPStatus.OK,
    path="",
    response_model=ListedResourcesResponse[EHRContextItem],
)
async def get_ehr_context_items(
    patient_id: str,
    ehr_contexts_service: EHRContextsService = Depends(get_ehr_contexts_service),
) -> ListedResourcesResponse[EHRContextItem]:
    items = await ehr_contexts_service.list_ehr_contexts_by_patient(
        patient_id=patient_id
    )

    return ListedResourcesResponse(items=items, total=len(items))
