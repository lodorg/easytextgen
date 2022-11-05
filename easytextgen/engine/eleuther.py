import json
import requests
from easytextgen.completion import CompletionParams
from easytextgen.engine.base import CompletionParamType, TextGenerationEngine


class EleutherEngine(TextGenerationEngine):
    models: list[str] = ["GPT-J-6B"]
    
    def __init__(self, model: str = "GPT-J-6B") -> None:
        self.model = model

    def get_available_parameters(self) -> list:
        return super().get_available_parameters() + [
            CompletionParamType.TEMPERATURE, 
            CompletionParamType.TOP_P, 
            CompletionParamType.MAX_GENERATED_TOKENS
        ]

    def on_generate(self, text: str, params: CompletionParams) -> str:
        json_parameters = json.dumps({
            "context": text,
            "topP": params.top_p,
            "temp": params.temperature,
            "response_length": params.max_generated_tokens,
            "remove_input": True,
        })
        response = requests.post("https://api.eleuther.ai/completion", data=json_parameters).json()
        try:
            return response[0]["generated_text"]
        except Exception as e:
            raise RuntimeError(response)