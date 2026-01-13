import uuid
from typing import AsyncGenerator, Generator

import asyncpg
import dotenv
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from testcontainers.postgres import PostgresContainer  # type: ignore  # fmt: skip

from app.app import create_app
from app.core.app_settings import get_app_settings, reset_app_settings_cache


@pytest.fixture(scope="session", autouse=True)
def load_env_vars() -> None:
    dotenv.load_dotenv(dotenv.find_dotenv(".env.test"), override=True)


@pytest.fixture(scope="session")
def db_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:17-alpine", driver=None) as postgres:
        yield postgres


@pytest_asyncio.fixture(autouse=True)
async def database_env(
    db_container: PostgresContainer,
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncGenerator[None, None]:
    admin_db_url = db_container.get_connection_url()
    dynamic_db_name = f"integration-test_{uuid.uuid4().hex}"

    conn = await asyncpg.connect(admin_db_url)
    try:
        await conn.execute(f'CREATE DATABASE "{dynamic_db_name}"')
    finally:
        await conn.close()

    monkeypatch.setenv("DB_HOST", db_container.get_container_host_ip())
    monkeypatch.setenv("DB_PORT", str(db_container.get_exposed_port(5432)))
    monkeypatch.setenv("DB_NAME", dynamic_db_name)
    monkeypatch.setenv("DB_USER", db_container.username)
    monkeypatch.setenv("DB_PASSWORD", db_container.password)

    reset_app_settings_cache()

    settings = get_app_settings()
    assert settings.db_name.startswith(
        "integration-test_",
    ), "Test environment must never connect to a non-test database"

    yield

    conn = await asyncpg.connect(admin_db_url)
    try:
        await conn.execute(
            """
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = $1
            """,
            dynamic_db_name,
        )
        await conn.execute(f'DROP DATABASE "{dynamic_db_name}"')
    finally:
        await conn.close()


@pytest_asyncio.fixture()
async def app() -> AsyncGenerator[FastAPI, None]:
    app = create_app()
    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        yield client
