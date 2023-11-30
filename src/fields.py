import json
from dataclasses import dataclass
from typing import Optional
from collections import defaultdict


@dataclass
class Field:
    name: str
    multiple: bool
    label: str
    type: str
    options: Optional[list[str]] = None
    qa_pipeline: Optional[str] = None


@dataclass
class Example:
    product_description: str
    output: str


def fields_metadata_from_json(path: str) -> dict[str, Field]:
    registry = {}
    with open(path) as f:
        for field in json.load(f):
            registry[field['name']] = Field(**field)
    return registry


def examples_from_json(path: str) -> dict[str, list[Example]]:
    coll = defaultdict(list)
    with open(path) as f:
        for example in json.load(f):
            coll[example['field_name']].append(
                Example(
                    output=example['field_value'],
                    product_description=example['LIBL_LIBELLE'],
                )
            )
    return coll
