import os

from langchain_openai import AzureChatOpenAI, ChatOpenAI

from .llm_base import LLMBase

from settings import get_settings


class AzureOpenAILLM(LLMBase):
    def __init__(self, model_name: str = "gpt-35-turbo", temperature: float = 0.1):
        super().__init__(model_name, temperature)
        # The API version you want to use: set this to `2023-12-01-preview` for the released version.
        os.environ["OPENAI_API_VERSION"] = get_settings().OPENAI_API_VERSION
        # The base URL for your Azure OpenAI resource.
        os.environ["AZURE_OPENAI_ENDPOINT"] = get_settings().AZURE_OPENAI_ENDPOINT
        # The API key for your Azure OpenAI resource.
        os.environ["AZURE_OPENAI_API_KEY"] = get_settings().AZURE_OPENAI_API_KEY

        self.temperature = temperature
        # Create an instance of Azure OpenAI
        # Replace the deployment name with your own
        self.llm = AzureChatOpenAI(
            deployment_name=model_name,
            temperature=self.temperature,
        )


class OpenAIProxyLLM(LLMBase):
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.1):
        super().__init__(model_name, temperature)

        self.llm = ChatOpenAI(
            api_key=get_settings().OPENAI_KEY,
            temperature=self.temperature,
        )
