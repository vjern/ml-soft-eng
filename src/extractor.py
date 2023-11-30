import random
import time
from enum import Enum

from fields import fields_metadata_from_json, examples_from_json, Field, Example

FIELD_METAS = fields_metadata_from_json("data/fields.json")
FIELD_EXAMPLES = examples_from_json("data/examples.json")


SYSTEM_PROMPT = (
    "Tu es un assistant qui m'aide à extraire des valeurs depuis un produit."
)
ENTRY_TEMPLATE = """
Product description: {product_description}
Attribute: {attribute}
""".strip()


class Models(Enum):
    CameLLM = "camellm"
    LLaMA = "llama"


class Extractor:
    prompt_max_size: int = -1
    prompt_template: str = "{system_prompt} {user_message}"
    entry_template: str = """
Product description: {description}
Attribute: {attribute}
"""

    def send_prompt(self, prompt: str) -> str:
        """
        Return placeholder
        """
        # Emulate latency in LLM response
        time.sleep(2)
        return f"Answer {self.__class__.__name__}"

    def build_prompt(
        self,
        product_description: str,
        field_id: str,
        nb_examples: int = 3,
    ) -> str:
        field_meta = FIELD_METAS.get(field_id)
        if field_meta is None:
            raise RuntimeError("No such extraction field: %s" % field_id)
        available_examples = FIELD_EXAMPLES[field_id]

        user_message_parts = []

        if nb_examples > 0:
            examples = random.choices(
                available_examples, k=min(len(available_examples), nb_examples)
            )
            for example in examples:
                print(f"{example = }")
                example_prompt_parts = [
                    ENTRY_TEMPLATE.format(
                        product_description=example.product_description,
                        attribute=field_meta.label,
                    )
                ]
                if field_meta.options:
                    example_prompt_parts.append(
                        "Options: " + ", ".join(field_meta.options)
                    )
                example_prompt_parts.append("Answer: " + example.output)
                print(f"{ example_prompt_parts = }")
                user_message_parts.append("\n".join(example_prompt_parts))
                user_message_parts.append("")

        user_message_parts.append(
            ENTRY_TEMPLATE.format(
                product_description=product_description,
                attribute=field_meta.label,
            )
        )

        prompt = self.prompt_template.format(
            system_prompt=SYSTEM_PROMPT,
            user_message="\n".join(user_message_parts).strip(),
        )
        return prompt

    def extract(
        self,
        product_description: str,
        field_id: str,
        nb_examples: int = 3,
    ) -> tuple[str, str]:
        """
        Extract a given field (referenced by its id) from a product description.
        Using a list of field examples, we also allow adding a number of examples
        to the prompt for the LLM to draw from.
        """
        prompt = self.build_prompt(product_description, field_id, nb_examples)
        if len(prompt) > self.prompt_max_size:
            raise Exception(
                f"Model {self.__class__.__name!r} prompt max size is {self.prompt_max_size}, got {len(prompt)}"
            )
        return self.send_prompt(prompt), prompt.strip()


def get_extractor(model: Models) -> Extractor:
    cls = {
        Models.CameLLM: Camell,
        Models.LLaMA: LLaMA,
    }[model]
    return cls()


class LLaMA(Extractor):
    prompt_max_size: int = 4096
    prompt_template: str = """
<s>[INST] <<SYS>>
{system_prompt}
<</SYS>>

{user_message} [/INST]
"""


class Camell(Extractor):
    prompt_max_size: int = 2048
    prompt_template: str = """
<s>### System prompt
{system_prompt}

### User Message
{user_message}
"""
