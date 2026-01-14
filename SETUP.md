# Setup Instructions

This document describes how to run the EHR Context Engineering demo locally.

## Local Setup Instructions

### Prerequisites

1. Python 3.12 installed on your machine.
2. Docker installed for containerized services (e.g., PostgreSQL).
3. uv v0.9 installed for dependency management. [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/)

### Setup Steps

#### 1. Sync Dependencies with `uv`

Sync your project dependencies (a new venv will be created if needed):

```bash
uv sync
```

#### 2. Activate the Virtual Environment

```bash
source .venv/bin/activate
```
#### 3. Set Up Environment Variables
Create a `.env` file in the project root directory with content found in the `.env.local` file. Update the values as needed. Do not commit the `.env` file to version control.

#### 4. Run tests (All tests should pass!)

```bash
uv run pytest
```

Note: Depending on your OS there might be some hipcups with the postgresql test container. If you run into issues in macos, just try again if it still does not work, please skip running the tests and reach out.

#### 5. Start DB

Prerequisite: Make sure Docker is installed on your machine, and docker-compose is available.

Please note the db is ephemeral and will be reset on each start/stop. This is the intended behavior.

Option 1 (preferred):

In a separate terminal, run:

```bash
docker compose up
```

To stop the db, just Ctrl+C, or (in separate terminal):
```bash
docker compose down
```

Seeing "ERROR: 2" after Ctrl+C is expected and can be ignored.

#### 6. Start the App
```bash
uv run python src/run.py
```

#### 7. Access the API docs to play with the demo

Open your browser and navigate to: [http://localhost:8000](http://localhost:8000). FastAPI automatically generates interactive API documentation. Open this link for more information: [FastAPI Swagger UI](https://fastapi.tiangolo.com/features/#automatic-docs).

Note: When posting ehr records, please start with the provided ehr record. Please notice the pydantic validation is very strict, and I did not take the time to make it more flexible.
