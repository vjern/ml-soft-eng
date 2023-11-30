from typing import Optional

from pydantic import BaseModel

from extractor import Models


class ExtractionTask(BaseModel):
    product_description: str
    fields_to_extract: list[str]


class ExtractionResult(BaseModel):
    field_name: str
    field_value: str
    prompt: Optional[list[str]]
    product_description: str


class PostExtract:
    class Request(BaseModel):
        model: Models
        tasks: list[ExtractionTask]

    class Response(BaseModel):
        results: list[ExtractionResult]
