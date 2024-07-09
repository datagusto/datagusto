import base64
from typing import Union

from core.llm_adapter.factory import LlmFactory


def encode_binary(value) -> Union[str, bytes]:
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("utf-8")
    else:
        return value


def query_llm(prompt: str) -> str:
    factory = LlmFactory()
    llm = factory.get_llm()
    return llm.completion(prompt)
