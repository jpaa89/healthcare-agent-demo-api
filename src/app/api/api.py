from fastapi import APIRouter, FastAPI
from fastapi.responses import RedirectResponse

from app.api.ehr_ingestion_tasks_api import router as ehr_ingestion_tasks_api


def setup_api(app: FastAPI) -> None:

    if app.docs_url:

        @app.get("/", include_in_schema=False)
        def _redirect_to_docs() -> RedirectResponse:  # pyright: ignore
            return RedirectResponse(url=str(app.docs_url))

    api = APIRouter(prefix="/api")

    api.include_router(
        ehr_ingestion_tasks_api,
        prefix="/ehr-ingestion-tasks",
        tags=["Electronic Health Record Ingestion Tasks API"],
    )

    app.include_router(api)
