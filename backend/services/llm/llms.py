import os

from langchain_openai import AzureChatOpenAI, ChatOpenAI

from .llm_base import LLMBase


class AzureOpenAILLM(LLMBase):
    def __init__(self, model_name: str = None, temperature: float = 0.1):
        model_name = model_name or os.getenv("AZURE_OPENAI_MODEL_NAME", "gpt-35-turbo")
        super().__init__(model_name, temperature)

        self.temperature = temperature
        # Create an instance of Azure OpenAI
        # Replace the deployment name with your own
        self.llm = AzureChatOpenAI(
            deployment_name=model_name,
            temperature=self.temperature,
        )


class OpenAILLM(LLMBase):
    def __init__(self, model_name: str = None, temperature: float = 0.1):
        model_name = model_name or os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
        super().__init__(model_name, temperature)

        self.llm = ChatOpenAI(
            api_key=os.environ["OPENAI_KEY"],
            temperature=self.temperature,
        )
