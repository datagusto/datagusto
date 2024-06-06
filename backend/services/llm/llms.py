import os
import re
from logging import getLogger
from typing import Any

import torch
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM

from .llm_base import LLMBase

logger = getLogger("uvicorn.app")


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


class LocalLLM(LLMBase):
    tokenizer: Any
    token: str
    device: str

    def __init__(self, model_name: str = None, temperature: float = 0.1):
        model_name = model_name or os.getenv("HUGGING_FACE_MODEL_NAME", "microsoft/Phi-3-mini-4k-instruct")
        super().__init__(model_name, temperature)

        self.device = os.getenv("USE_GPU", "cpu")
        self.token = os.getenv("HUGGING_FACE_ACCESS_TOKEN")
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=model_name,
            trust_remote_code=True,
            token=self.token
        )

        if self.device == "mps":
            torch.set_default_device("mps")
            self.llm = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name,
                trust_remote_code=True,
                device_map="auto",
                low_cpu_mem_usage=True,
                token=self.token
            )
            logger.debug("Using Apple M1 GPU...")
        else:
            self.llm = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name,
                trust_remote_code=True,
                low_cpu_mem_usage=True,
                token=self.token
            )
            logger.debug("Using CPU...")
        logger.debug("Loaded model: %s", model_name)

    def completion(self, prompt: str, max_token: int = 100, **kwargs) -> str:
        if self.device == "mps":
            model_inputs = self.tokenizer([prompt], return_tensors="pt").to("mps")
        else:
            model_inputs = self.tokenizer([prompt], return_tensors="pt")
        generated_ids = self.llm.generate(**model_inputs, max_new_tokens=max_token)
        result = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        try:
            response = self.remove_prompt_from_response(prompt, result[0])
        except Exception as e:
            logger.exception("Error removing prompt from response.")
            response = result[0]
        return response

    def remove_prompt_from_response(self, prompt: str, response: str) -> str:
        """
        Remove the given prompt from the start of the response.

        Args:
            prompt (str): The prompt to remove.
            response (str): The response containing the prompt.

        Returns:
            str: The response with the prompt removed.
        """
        # Escape any special characters in the prompt to prevent regex issues
        escaped_prompt = re.escape(prompt)
        # Use regex to remove the prompt from the start of the response
        clean_response = re.sub(f'^{escaped_prompt}', '', response).strip()

        return clean_response
