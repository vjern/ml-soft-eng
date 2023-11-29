from pydantic import BaseModel

from extractor import Models


class Task(BaseModel):
    # and other fields
    ctx: dict[str, str]
    fields_to_extract: list[str]

    def full_text(self) -> str:
        return "\n".join(
            "%s: %s" % (key, value)
            for key, value in self.ctx.items()
        )


class Extraction:

    class Request(BaseModel):
        model: Models
        tasks: list[Task]

    class Response(BaseModel):
        class ExtractionResult(BaseModel):
            attributes: dict[str, str]
            task: Task
        results: list[ExtractionResult]
