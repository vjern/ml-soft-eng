import json
from dataclasses import dataclass
from typing import Optional
from collections import defaultdict


"""
Loading utilities and schemas for extraction field metadata & examples
"""


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
    successful: bool = False


def fields_metadata_from_json(path: str) -> dict[str, Field]:
    registry = {}
    with open(path) as f:
        for field in json.load(f):
            registry[field["name"]] = Field(**field)
    return registry


def examples_from_json(
    path: str,
    include_all: bool = False,
) -> dict[str, list[Example]]:
    coll = defaultdict(list)
    with open(path) as f:
        for example in json.load(f):
            if include_all or example["field_value"] is not None:
                coll[example["field_name"]].append(
                    Example(
                        output=example["field_value"],
                        # We make the choice to use this property as the main description of the product
                        product_description=example["LIBL_LIBELLE"],
                    )
                )
    return coll
