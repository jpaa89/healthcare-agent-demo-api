from datetime import datetime, timezone
from typing import Sequence
from uuid import uuid4

from app.domain.ehr_ingestion.ehr_context_models import (
    EHRContextItem,
    EHRContextSource,
    EHRContextType,
    EHRSourceType,
)
from app.domain.ehr_ingestion.ehr_contexts_repository import EhrContextsRepository
from app.domain.ehr_ingestion.ehr_models import ElectronicPatientRecord


class EHRContextsService:

    def __init__(self, ehr_contexts_repository: EhrContextsRepository):
        self.ehr_contexts_repository = ehr_contexts_repository

    async def ingest_ehr(self, ehr: ElectronicPatientRecord) -> None:
        items: list[EHRContextItem] = []

        now = datetime.now(timezone.utc)
        patient_id = ehr.patient_id

        # Demographics
        items.append(
            EHRContextItem(
                id=uuid4(),
                patient_id=patient_id,
                type=EHRContextType.DEMOGRAPHICS,
                content=(
                    f"{ehr.demographics.name}, "
                    f"{ehr.demographics.age} years old, "
                    f"gender {ehr.demographics.gender}, "
                    f"blood type {ehr.demographics.blood_type}"
                ),
                data=ehr.demographics.model_dump(),
                source=EHRContextSource(
                    type=EHRSourceType.DEMOGRAPHICS,
                    recorded_at=None,
                    recorded_by=None,
                ),
                created_at=now,
            )
        )

        # Chronic conditions
        for condition in ehr.medical_history.chronic_conditions:
            items.append(
                EHRContextItem(
                    id=uuid4(),
                    patient_id=patient_id,
                    type=EHRContextType.CHRONIC_CONDITION,
                    content=condition,
                    data={"condition": condition},
                    source=EHRContextSource(
                        type=EHRSourceType.MEDICAL_HISTORY,
                        recorded_at=None,
                        recorded_by=None,
                    ),
                    created_at=now,
                )
            )

        # Allergies
        for allergy in ehr.medical_history.allergies:
            items.append(
                EHRContextItem(
                    id=uuid4(),
                    patient_id=patient_id,
                    type=EHRContextType.ALLERGY,
                    content=f"Allergy to {allergy}",
                    data={"allergy": allergy},
                    source=EHRContextSource(
                        type=EHRSourceType.MEDICAL_HISTORY,
                        recorded_at=None,
                        recorded_by=None,
                    ),
                    created_at=now,
                )
            )

        # Medications
        for med in ehr.medical_history.current_medications:
            items.append(
                EHRContextItem(
                    id=uuid4(),
                    patient_id=patient_id,
                    type=EHRContextType.MEDICATION,
                    content=f"{med.name}, {med.dose}, {med.frequency}",
                    data=med.model_dump(),
                    source=EHRContextSource(
                        type=EHRSourceType.MEDICAL_HISTORY,
                        recorded_at=None,
                        recorded_by=None,
                    ),
                    created_at=now,
                )
            )

        # Visits
        for visit in ehr.recent_visits:
            items.append(
                EHRContextItem(
                    id=uuid4(),
                    patient_id=patient_id,
                    type=EHRContextType.VISIT,
                    content=f"{visit.reason}. {visit.notes}",
                    data=visit.model_dump(),
                    source=EHRContextSource(
                        type=EHRSourceType.DOCTOR,
                        recorded_at=visit.date,
                        recorded_by=visit.doctor,
                    ),
                    created_at=now,
                )
            )

        # Lab results

        for lab in ehr.lab_results:
            lab_result_content = ", ".join(f"{k}={v}" for k, v in lab.results.items())
            lab_result_content = f"Lab Test - {lab.test}: {lab_result_content}"
            items.append(
                EHRContextItem(
                    id=uuid4(),
                    patient_id=patient_id,
                    type=EHRContextType.LAB_RESULT,
                    content=lab_result_content,
                    data={
                        "date": lab.date,
                        "test": lab.test,
                        "results": lab.results,
                    },
                    source=EHRContextSource(
                        type=EHRSourceType.LAB_TEST,
                        recorded_at=lab.date,
                        recorded_by=None,
                    ),
                    created_at=now,
                )
            )

        await self.ehr_contexts_repository.delete_by_patient_id(patient_id)
        await self.ehr_contexts_repository.insert_many(items)

    async def list_ehr_contexts_by_patient(
        self, patient_id: str
    ) -> Sequence[EHRContextItem]:
        return await self.ehr_contexts_repository.list_by_patient(patient_id)
