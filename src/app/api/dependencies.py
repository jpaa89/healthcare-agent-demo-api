import asyncpg
from fastapi import Depends, Request
from typing import cast

from app.domain.ehr_ingestion.ehr_contexts_service import EHRContextsService
from app.domain.ehr_ingestion.ehr_contexts_repository import EhrContextsRepository

from typing import AsyncGenerator


async def get_db_conn(request: Request) -> AsyncGenerator[asyncpg.Connection, None]:
    pool: asyncpg.Pool = request.app.state.pool
    async with pool.acquire() as connection:
        yield cast(asyncpg.Connection, connection)


async def get_ehr_contexts_repository(
    conn: asyncpg.Connection = Depends(get_db_conn),
) -> EhrContextsRepository:
    return EhrContextsRepository(conn=conn)


async def get_ehr_contexts_service(
    ehr_contexts_repository: EhrContextsRepository = Depends(
        get_ehr_contexts_repository
    ),
) -> EHRContextsService:
    return EHRContextsService(ehr_contexts_repository=ehr_contexts_repository)
