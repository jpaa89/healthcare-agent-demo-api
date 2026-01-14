from typing import Generic, Sequence, TypeVar
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class CreatedResourceResponse(BaseModel):
    id: UUID


class ListedResourcesResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
