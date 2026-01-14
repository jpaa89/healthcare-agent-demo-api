from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, Path

from app.api.dependencies import get_ehr_query_service
from app.domain.ehr_query.ehr_query_models import EHRQuery, EHRQueryOutput
from app.domain.ehr_query.ehr_query_service import EHRQueryService


router = APIRouter()


@router.post(
    path="/{patient_id}/query",
    status_code=HTTPStatus.OK,
    response_model=EHRQueryOutput,
)
async def query_ehr(
    patient_id: str = Path(..., description="EHR Patient Id"),
    ehr_query: EHRQuery = Body(...),
    ehr_query_service: EHRQueryService = Depends(get_ehr_query_service),
) -> EHRQueryOutput:
    return await ehr_query_service.query(patient_id=patient_id, ehr_query=ehr_query)
