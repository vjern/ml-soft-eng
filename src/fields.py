import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExtractField:
    name: str
    multiple: bool
    label: str
    type: str
    options: Optional[list[str]] = None
    qa_pipeline: Optional[str] = None


def from_json(path: str) -> dict[str, ExtractField]:
    registry = {}
    with open(path) as f:
        for field in json.load(f):
            registry[field['name']] = ExtractField(**field)
    return registry
