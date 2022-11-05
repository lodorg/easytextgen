import json
import requests
from easytextgen.completion import CompletionParams
from easytextgen.engine.base import CompletionParamType, TextGenerationEngine


class ForefrontEngine(TextGenerationEngine):
    models: list[str] = ["gpt-j-6b-vanilla"]
    
    def __init__(self, endpoint: str, api_key: str) -> None:
        self.endpoint = endpoint
        self.api_key = api_key

    def get_available_parameters(self) -> list:
        return super().get_available_parameters() + [
            CompletionParamType.TEMPERATURE,
            CompletionParamType.TOP_K,
            CompletionParamType.TOP_P,
            CompletionParamType.REPETITION_PENALTY,
            CompletionParamType.MAX_GENERATED_TOKENS
        ]

    def on_generate(self, text: str, params: CompletionParams) -> str:
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "text": text,
            "top_p": params.top_p,
            "top_k": params.top_k,
            "temperature": params.temperature,
            "repetition_penalty": params.repetition_penalty,
            "length": params.max_generated_tokens,
            "stop_sequences": [params.stop_string],
        }

        res = requests.post(
            self.endpoint,
            json=body,
            headers=headers
        )
        
        try:
            return res.json()["result"][0]["completion"]
        except Exception as e:
            raise RuntimeError(res)
