import os
import uuid
from datetime import datetime
from typing import Optional

import pytz
import requests
from dotenv import load_dotenv

from .llm_base import LLMBase

load_dotenv(".custom.env")


class CustomProxyLLM(LLMBase):
    token: str
    embed_url: str = None
    generation_url: str = None

    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.1, **kwargs):
        super().__init__(model_name, temperature)
        self.token = os.environ["CUSTOM_PROXY_TOKEN"]
        self.embed_url = os.environ["CUSTOM_PROXY_EMBED_URL"]
        self.generation_url = os.environ["CUSTOM_PROXY_GENERATION_URL"]
        self.llm = None

    # @retry_post
    def embed(self, text: str, model_id: str = "text-embedding-ada-002"):
        """Get the embedding for a given text using the specified model"""
        payload = {
            "modelId": model_id,
            "text": text,
        }

        # Make the request
        response = requests.request(
            "POST",
            self.embed_url,
            headers=self._generate_headers(),
            json=payload,
        )
        data = response.json()
        print(data)

        return data

    # @retry_post
    def completion(
            self,
            prompt: str,
            role: Optional[str] = None,
            model_name: Optional[str] = None,
            temperature: Optional[float] = None,
            **kwargs,
    ):
        """Generate the completion for a given prompt

        prompt: str
            The prompt to generate a completion for
        role: str
            The role of the prompt
        model_name: str
            Model id of the model to use. if not provided, the default model will be used
        temperature: float
            The temperature to use for the completion. If not provided, the default temperature will be used

        kwargs:
            frequencyPenalty: float
            maxTokens: int
            presencePenalty: float
            seed: int
            stops: list[str]
            toolChoice: str
            tools: list

        """
        _model_name = model_name or self.model_name
        _temperature = temperature or self.temperature
        payload = {
            "chatCompletionMessages": [
                {
                    "prompt": prompt,
                    "promptRole": role,
                }
            ],
            "modelId": _model_name,
            "modelParam": {
                "openAi": {
                    "frequencyPenalty": kwargs.get("frequencyPenalty", 0.0),
                    "maxTokens": kwargs.get("maxTokens", 0),
                    "presencePenalty": kwargs.get("presencePenalty", 0.0),
                    "seed": kwargs.get("seed", 0),
                    "stops": kwargs.get("stops", []),
                    "temperature": _temperature,
                    "toolChoice": kwargs.get("toolChoice", None),
                    "tools": kwargs.get("tools", [])
                }
            }
        }

        response = requests.request(
            "POST",
            self.generation_url,
            headers=self._generate_headers(),
            json=payload
        )
        data = response.json()

        return data

    def _generate_headers(self) -> dict[str, str]:
        """Generate the headers for the API request"""
        headers = {
            "Content-Type": "application/json",
            "Request-ID": str(uuid.uuid1()),
            "Timestamp": pytz.utc.localize(datetime.utcnow()).isoformat(),
            "API-Key": self.token,
            "Authorization": os.environ["CUSTOM_PROXY_BASIC_AUTH_TOKEN"]
        }
        return headers
