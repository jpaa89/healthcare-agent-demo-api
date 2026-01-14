from app.domain.ehr_ingestion.ehr_contexts_repository import EhrContextsRepository
from app.domain.ehr_query.ehr_prompt_utils import (
    build_ehr_contexts_selection_prompt,
    build_grounded_query_output_prompt,
)
from app.domain.ehr_query.ehr_query_models import (
    EHRContextIds,
    EHRQuery,
    EHRQueryOutput,
)
from app.domain.llm.llm_client import LLMClient


class EHRQueryService:

    def __init__(
        self, ehr_contexts_repository: EhrContextsRepository, llm_client: LLMClient
    ):
        self.ehr_contexts_repository = ehr_contexts_repository
        self.llm_client = llm_client

    async def query(self, patient_id: str, ehr_query: EHRQuery) -> EHRQueryOutput:
        items = await self.ehr_contexts_repository.list_by_patient(patient_id)

        context_selection_prompt = build_ehr_contexts_selection_prompt(
            question=ehr_query.query,
            ehr_context_items=items,
        )

        relevant_items_ids = await self.llm_client.run_structured(
            prompt=context_selection_prompt,
            response_model=EHRContextIds,
        )

        relevant_items = [item for item in items if item.id in relevant_items_ids.ids]

        grounded_answer_prompt = build_grounded_query_output_prompt(
            question=ehr_query.query,
            ehr_context_items=relevant_items,
        )

        grounded_query_output = await self.llm_client.run(
            prompt=grounded_answer_prompt,
        )

        return EHRQueryOutput(
            answer=grounded_query_output,
            references=relevant_items,
        )
