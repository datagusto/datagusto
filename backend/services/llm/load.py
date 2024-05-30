import os
from typing import Optional

from .llm_base import LLMBase
from .llms import AzureOpenAILLM, OpenAILLM, LocalLLM

llm: Optional[LLMBase] = None

if os.environ["LLM_USAGE_TYPE"] == "AZURE_OPENAI":
    llm = AzureOpenAILLM()

if os.environ["LLM_USAGE_TYPE"] == "OPENAI":
    llm = OpenAILLM()

if os.environ["LLM_USAGE_TYPE"] == "LOCAL":
    llm = LocalLLM()

if os.environ["LLM_USAGE_TYPE"] == "CUSTOM_PROXY":
    from .custom_proxy_llm import CustomProxyLLM
    llm = CustomProxyLLM()

if llm is None:
    raise Exception("LLM is not configured properly. Please check LLM_USAGE_TYPE in .env file")
