from typing import Any
from enum import Enum


SYSTEM_PROMPT = "Tu es un assistant qui m'aide à extraire des valeurs depuis un produit."


class Models(Enum):
    CameLLM = 'camellm'
    LLaMA = 'llama'


class Extractor:
    prompt_max_size: int = -1
    prompt_template: str = "{system_prompt} {user_message}"

    def send_prompt(self, prompt: str) -> str:
        """
        Return placeholder
        """
        print(f"Prompted {self = } {prompt = }")
        return f"Answer {self.__class__.__name__}"

    def extract(self, text: str, attr: str) -> str:
        # check that attributes exist
        return attr + ":placeholder:" + text
        # build examples
        examples = []
        # build prompt
        user_message = "\n".join([
            *examples,
            text,
        ])
        return self.send_prompt(
            self.prompt_template.format(
                system_prompt=SYSTEM_PROMPT,
                user_message=user_message,
            )
        )
        if len(prompt) > self.prompt_max_size:
            raise Exception(
                f"Model {self.__class__.__name!r} prompt max size is {self.prompt_max_size}, got {len(prompt)}"
            )


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

def get_extractor(model_name: str) -> Extractor:
    cls = {
        Models.CameLLM: Camell,
        Models.LLaMA: LLaMA,
    }[Models(model_name)]
    return cls()
