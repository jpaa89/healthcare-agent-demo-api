from fastapi import FastAPI

from app.api.api import setup_api


def create_app() -> FastAPI:

    app = FastAPI(
        title="healthcare-agent-demo-api",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    setup_api(app)

    return app
