from typing import TypeVar, override
from openai import AsyncOpenAI

from app.domain.llm.llm_client import LLMClient

T = TypeVar("T")


class OpenAILLMClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-4.1-mini"):
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    @override
    async def run_structured(
        self,
        *,
        prompt: str,
        response_model: type[T],
    ) -> T:
        response = await self._client.responses.parse(
            model=self._model,
            input=prompt,
            text_format=response_model,
        )

        parsed = response.output_parsed
        if parsed is None:
            raise RuntimeError("LLM returned no structured output")

        return parsed

    @override
    async def run(self, *, prompt: str) -> str:
        response = await self._client.responses.create(
            model=self._model,
            input=prompt,
        )

        return response.output_text or ""
