import os
from logging import getLogger

from langchain_openai import AzureChatOpenAI, ChatOpenAI

from .llm_base import LLMBase

logger = getLogger("uvicorn.app")

DEFAULT_LOCAL_LLM = "mistralai/Mistral-7B-Instruct-v0.3"


class AzureOpenAILLM(LLMBase):
    def __init__(self, model_name: str = None, temperature: float = 0.1, **kwargs):
        logger.debug("Initializing Azure OpenAI LLM...")
        model_name = model_name or os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo")
        super().__init__(model_name, temperature)

        # Create an instance of Azure OpenAI
        # Replace the deployment name with your own
        self.llm = AzureChatOpenAI(
            deployment_name=model_name,
            temperature=self.temperature,
        )


class OpenAILLM(LLMBase):
    def __init__(self, model_name: str = None, temperature: float = 0.1, **kwargs):
        model_name = model_name or os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
        super().__init__(model_name, temperature)

        self.llm = ChatOpenAI(
            api_key=os.environ["OPENAI_KEY"],
            temperature=self.temperature,
        )
