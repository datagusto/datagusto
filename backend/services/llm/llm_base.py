from abc import ABC
from typing import Any, Optional


class LLMBase(ABC):
    temperature: float = 0.1
    model_name: str = "gpt-3.5-turbo"
    llm: Any

    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.1):
        self.temperature = temperature
        self.model_name = model_name

    def completion(
            self,
            prompt: str,
            role: Optional[str] = None,
            model_name: Optional[str] = None,
            temperature: Optional[float] = None,
            **kwargs,
    ):
        res = self.llm.invoke(prompt)
        return str(res.content)
