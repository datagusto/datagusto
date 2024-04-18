from typing import Optional

from .llm_base import LLMBase
from .llms import AzureOpenAILLM, OpenAIProxyLLM
from settings import get_settings

llm: Optional[LLMBase] = None

if get_settings().LLM_USAGE_TYPE == "AZURE_OPENAI":
    llm = AzureOpenAILLM()

if get_settings().LLM_USAGE_TYPE == "OPENAI":
    llm = OpenAIProxyLLM()

if get_settings().LLM_USAGE_TYPE == "CUSTOM_PROXY":
    from .custom_proxy_llm import CustomProxyLLM
    llm = CustomProxyLLM()

if llm is None:
    raise Exception("LLM is not configured properly. Please check LLM_USAGE_TYPE in .env file")
