from enum import Enum
from typing import Any

from pydantic import BaseModel


class LLMEnum(Enum):
    CameLLM = 'camel'
    LLaMA = 'lama'


class ExtractRequest(BaseModel):
    model: LLMEnum
    attributes: list[str]
    content: str


class ExtractResponse(BaseModel):
    objects: dict[str, Any]