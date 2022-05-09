import attr
import requests

from easytextgen.completion import CompletionParams
from easytextgen.engine.base import TextGenerationEngine


@attr.s
class VicgalleEngine(TextGenerationEngine):
    model: str = attr.ib(default="GPT-J-6B")
    models: list[str] = ["GPT-J-6B"]

    def __init__(self, model: str) -> None:
        self.model = model

    def get_available_parameters(self) -> list[str]:
        return super().get_available_parameters() + ["temperature", "top_p", "max_generated_tokens"]

    def on_generate(self, text: str, params: CompletionParams) -> str:
        payload = {
            "context": text,
            "token_max_length": params.max_generated_tokens,
            "temperature": params.temperature,
            "top_p": params.top_p,
        }
        response = requests.post("http://api.vicgalle.net:5000/generate", params=payload).json()
        try:
            return response["text"]
        except Exception as e:
            raise RuntimeError(response)