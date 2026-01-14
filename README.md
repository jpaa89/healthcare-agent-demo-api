# EHR Context Engineering Demo

## Setup Instructions

See [SETUP.md](./SETUP.md) for instructions on how to run this demo locally.

## Overview

This project is a **technical demo** that implements a context engineering pipeline for an AI-assisted clinical system.

The goal is to demonstrate how AI can assist a physician during consultations by:
- ingesting Electronic Health Record (EHR) data,
- decomposing it into structured, traceable context items,
- selectively retrieving relevant information based on a physician’s question,
- and generating grounded answers with explicit references to the source data.

This is **not a production-ready clinical system**, but a focused demonstration of architecture, reasoning, and trade-off awareness.

---

## Problem Being Addressed

Clinical data is usually complex, heterogeneous, and highly sensitive.  
Naively sending full patient records to an LLM is unsafe, inefficient, and untraceable.

This demo explores:
- how to **structure raw EHR data into atomic context units**,
- how to **retrieve only what is relevant** for a given question,
- and how to ensure **grounding and provenance** in AI-generated answers.

---

## Selected Technologies

### Python 3.12
- Modern and solid Python version.
- Good ecosystem for async I/O, APIs, and data modeling and ai integrations.

### FastAPI
- Clear request/response modeling.
- Dependency injection makes architecture explicit.
- Well suited for API-first designs and demos.

### asyncpg + PostgreSQL
- Async, non-blocking database access.
- PostgreSQL provides JSON support and strong consistency.
- Simple and reliable for structured context storage.

### Pydantic
- Strong data validation for:
  - EHR inputs
  - Domain models
  - API responses
  - LLM structured outputs
- Used intentionally to enforce **contracts**, not just convenience.
- Please note that some validations are very strict for EHR records just for demo purposes and convenience, the models can be relaxed depending on real requirements.

### OpenAI API (Responses API)
- LLMs assist with relevance selection and answer synthesis.
- Structured outputs are used where correctness matters.
- Generic interfaces allow swapping LLM providers.

### Pytest + HTTPX + Testcontainers
- Just for some very basic testing for ingestion and context building.

---

## Architecture Overview

This project follows a **pragmatic interpretation of Clean Architecture and the repository pattern**.

The intent is to clearly separate concerns, while acknowledging that:
- this is a demo,
- some compromises are intentional,
- and the architecture is not “pure” or fully generalized (for example there are no repository abstractions or unit of work implementations).

### Key architectural principles

- **Domain logic does not depend on vendors**
- **LLM usage is explicit, constrained, and optional**
- **All answers must be grounded in stored context items**

## Context Engineering Design

### 1. EHR Ingestion

Incoming EHR data is ingested as a typed domain model and deterministically decomposed into **EHRContextItem** records.

Each context item:
- represents a single clinical fact,
- has a clear `type` (medication, allergy, visit, lab, etc.),
- includes human-readable `content`,
- stores structured `data`,
- and carries provenance metadata (source, date, author when available).

This decomposition is **deterministic** and does not use LLMs.

Note: There is a mocked task uuid generator for EHR documents and context items for demo purposes. Just to hint this could be part of a more complex ingestion pipeline with background tasks.

---

### 2. Context Storage

Context items are persisted individually in the database.

This enables:
- fine-grained retrieval,
- explicit grounding,
- and selective exposure to AI models.

Raw EHR documents are never passed directly to the LLM.

---

### 3. Query Flow

When a physician asks a question:

1. All context items for the patient are retrieved.
2. An LLM is used **only to assist in selecting relevant context items**.
3. A second LLM call synthesizes a **grounded answer** using only the selected contexts.
4. The LLM must return:
   - the answer text
   - the IDs of the context items it used
5. The API resolves those IDs back to full context objects and returns them as references.

At no point is the LLM allowed to invent facts or access data outside the provided context.

---

## LLM Usage Philosophy

LLMs are treated as:
- **assistive components**, not decision-makers,
- tools for ranking and synthesis,
- and always constrained by explicit contracts.

Key safeguards:
- Structured outputs
- Closed-world prompts
- Post-validation of returned IDs

---

## Trade-offs and Pragmatism

This demo intentionally makes trade-offs:

- No embeddings or vector databases (kept out of scope)
- No background task orchestration
- Schema creation at startup instead of migrations

These decisions were made to:
- keep the system easy to reason about,
- maximize clarity in a technical assessment,
- and focus on architectural correctness rather than completeness.

