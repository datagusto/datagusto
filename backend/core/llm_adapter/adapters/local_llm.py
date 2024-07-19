import os
import re
from logging import getLogger
from typing import Any

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .llm_base import LLMBase

logger = getLogger("uvicorn.app")

DEFAULT_LOCAL_LLM = "mistralai/Mistral-7B-Instruct-v0.3"


class LocalLLM(LLMBase):
    tokenizer: Any
    token: str
    device: str
    instruction_models: list[str] = [DEFAULT_LOCAL_LLM]

    def __init__(self, model_name: str = None, temperature: float = 0.1):
        model_name = model_name or os.getenv("HUGGING_FACE_MODEL_NAME", DEFAULT_LOCAL_LLM)
        super().__init__(model_name, temperature)

        self.device = os.getenv("USE_GPU", "cpu")
        self.token = os.getenv("HUGGING_FACE_ACCESS_TOKEN")
        self.tokenizer = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=model_name,
            trust_remote_code=True,
            token=self.token,
        )

        if self.device == "cuda":
            torch.set_default_device("cuda")
            self.llm = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name,
                trust_remote_code=True,
                device_map="auto",
                low_cpu_mem_usage=True,
                token=self.token,
            )
            logger.debug("Using GPU...")
        elif self.device == "mps":
            torch.set_default_device("mps")
            self.llm = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name,
                trust_remote_code=True,
                device_map="auto",
                low_cpu_mem_usage=True,
                token=self.token,
            )
            logger.debug("Using Apple M1 GPU...")
        else:
            self.llm = AutoModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path=model_name,
                trust_remote_code=True,
                low_cpu_mem_usage=True,
                token=self.token,
            )
            logger.debug("Using CPU...")
        logger.debug("Loaded model: %s", model_name)

    def completion(self, prompt: str, max_token: int = 100, **kwargs) -> str:
        complete_prompt = self.format_prompt_for_completion(prompt)
        if self.device == "cuda":
            model_inputs = self.tokenizer([complete_prompt], return_tensors="pt").to("cuda")
        elif self.device == "mps":
            model_inputs = self.tokenizer([complete_prompt], return_tensors="pt").to("mps")
        else:
            model_inputs = self.tokenizer([complete_prompt], return_tensors="pt")
        generated_ids = self.llm.generate(
            **model_inputs,
            max_new_tokens=max_token,
            do_sample=True,
            temperature=self.temperature,
        )
        result = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
        logger.debug("Result: %s", result[0])
        try:
            response = self.remove_prompt_from_response(prompt, result[0])
            logger.debug("Response: %s", response)
        except Exception:
            logger.exception("Error removing prompt from response.")
            response = result[0]
        return response

    def format_prompt_for_completion(self, prompt: str) -> str:
        complete_prompt = prompt
        if self.model_name in self.instruction_models:
            complete_prompt = f"""[INST]{prompt}
            [/INST]
            """
        return complete_prompt

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
        clean_response = re.sub(f"^{escaped_prompt}", "", response).strip()

        return clean_response
