from typing import Generic, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class Response(GenericModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T]
    errors: Optional[dict] = None
