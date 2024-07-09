import os

from .adapters.azureai_endpoint import AzureAIEndpoint
from .adapters.llm_base import LLMBase
from .adapters.llms import AzureOpenAILLM, OpenAILLM
from .adapters.local_llm import LocalLLM

ADAPTERS = {
    'AZURE_OPENAI': AzureOpenAILLM,
    "OPENAI": OpenAILLM,
    "LOCAL": LocalLLM,
    "AZUREAI_ENDPOINT": AzureAIEndpoint,
    "CUSTOM_PROXY": "CustomProxyLLM"
}


class LlmFactory:

    def __init__(self):
        adapter_name = os.environ.get("LLM_USAGE_TYPE")
        if adapter_name not in ADAPTERS:
            raise ValueError(f"LLM is not configured properly. Please check LLM_USAGE_TYPE in .env file.")
        self.adapter_name = adapter_name

    def get_llm(self) -> "LLMBase":
        if self.adapter_name == "CUSTOM_PROXY":
            from .adapters.custom_proxy_llm import CustomProxyLLM
            return CustomProxyLLM()

        adapter = ADAPTERS[self.adapter_name]
        return adapter()
