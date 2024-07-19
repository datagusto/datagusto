import json
import os
from logging import getLogger
from typing import Optional

import requests

from .llm_base import LLMBase

logger = getLogger("uvicorn.app")


class AzureAIEndpoint(LLMBase):
    endpoint: str
    token: str

    def __init__(self, model_name: Optional[str] = None, temperature: float = 0.1) -> None:
        super().__init__(model_name, temperature)

        self.endpoint = os.environ["AZUREAI_ENDPOINT"]
        self.token = os.environ["AZUREAI_ENDPOINT_TOKEN"]
        logger.debug("AzureAI endpoint: %s", self.endpoint)

    def completion(self, prompt: str, max_token: int = 100, **kwargs: dict) -> str:
        try:
            response = requests.request(
                "POST",
                self.endpoint,
                headers=self._generate_headers(),
                data=self._generate_payload(prompt, max_token),
                timeout=60,
            )
            data = response.json()
            logger.debug("AzureAI response: %s", data)
            return self._generate_response(data)
        except Exception:
            logger.exception("Error happened while connecting to AzureAI Endpoint.")
            return ""

    def _generate_payload(self, prompt: str, max_token: int = 100, **kwargs: dict) -> str:
        payload = prompt
        if "inference.ai.azure.com" in self.endpoint:
            payload = json.dumps(
                {
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_token,
                    "temperature": self.temperature,
                    "top_p": 1,
                },
            )
        elif "inference.ml.azure.com" in self.endpoint:
            payload = json.dumps(
                {
                    "input_data": {
                        "input_string": [prompt],
                        "parameters": {"temperature": self.temperature, "top_p": 1, "max_new_tokens": max_token},
                    },
                },
            )

        return payload

    def _generate_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"}
        return headers

    def _generate_response(self, response: dict) -> str:
        response_message = json.dumps(response)
        if "inference.ai.azure.com" in self.endpoint:
            response_message = response["choices"][0]["message"]["content"]
        elif "inference.ml.azure.com" in self.endpoint:
            response_message = response[0]["0"]
        return response_message
