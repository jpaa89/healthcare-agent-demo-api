from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncpg
from fastapi import FastAPI

from app.api.api import setup_api
from app.core.app_settings import get_app_settings

CREATE_EHR_CONTEXT_TABLE = """
CREATE TABLE IF NOT EXISTS ehr_patient_context (
    id UUID PRIMARY KEY,
    patient_id TEXT NOT NULL,
    type TEXT NOT NULL,
    content TEXT NOT NULL,
    data JSONB,
    source_type TEXT NOT NULL,
    source_recorded_at DATE,
    source_recorded_by TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ehr_context_patient
    ON ehr_patient_context (patient_id);

CREATE INDEX IF NOT EXISTS idx_ehr_context_patient_type
    ON ehr_patient_context (patient_id, type);

"""


async def bootstrap_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(CREATE_EHR_CONTEXT_TABLE)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    app_settings = get_app_settings()
    database_url = (
        f"postgresql://{app_settings.db_user}:"
        f"{app_settings.db_password}@"
        f"{app_settings.db_host}:"
        f"{app_settings.db_port}/"
        f"{app_settings.db_name}"
    )
    try:
        pool = await asyncpg.create_pool(dsn=database_url)
        await bootstrap_schema(pool)
        app.state.pool = pool
        yield
    finally:
        await app.state.pool.close()


def create_app() -> FastAPI:

    app = FastAPI(
        title="healthcare-agent-demo-api",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    setup_api(app)

    return app
