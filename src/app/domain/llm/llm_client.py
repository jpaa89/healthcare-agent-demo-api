from abc import ABC, abstractmethod
from typing import Type, TypeVar
from uuid import UUID

from openai import BaseModel
from pydantic import ConfigDict

from app.domain.ehr_ingestion.ehr_context_models import EHRContextItem


T = TypeVar("T")


class LLMClient(ABC):

    @abstractmethod
    async def run_structured(
        self,
        *,
        prompt: str,
        response_model: Type[T],
    ) -> T: ...

    @abstractmethod
    async def run(
        self,
        *,
        prompt: str,
    ) -> str: ...
