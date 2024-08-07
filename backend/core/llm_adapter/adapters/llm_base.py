from abc import ABC
from typing import Any


class LLMBase(ABC):
    temperature: float
    model_name: str
    llm: Any

    def __init__(self, model_name: str, temperature: float = 0.1, **kwargs: dict) -> None:
        self.temperature = temperature
        self.model_name = model_name

    def completion(
        self,
        prompt: str,
        **kwargs: dict,
    ) -> str:
        res = self.llm.invoke(prompt)
        return str(res.content)
