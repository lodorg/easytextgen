import attr
import openai

from easytextgen import tokenizer
from easytextgen.completion import CompletionParams
from easytextgen.engine.base import CompletionParamType, TextGenerationEngine


class OpenAIEngine(TextGenerationEngine):
    """OpenAI's official GPT-3 API."""

    models: list[str] = [
        "ada", "babbage", "curie", "davinci", "cushman", 
        "davinci-instruct-beta", "curie-instruct-beta", 
        "davinci-codex", "cushman-codex",
    ]
    
    def __init__(self, api_key: str, model: str, goose_ai: bool = False) -> None:
        self.api_key: str = api_key
        self.model: str = model
        
        if goose_ai:
            openai.api_base = "https://api.goose.ai/v1"
        
        openai.api_key = self.api_key

    def get_available_parameters(self) -> list:
        return super().get_available_parameters() + [
            CompletionParamType.TEMPERATURE, 
            CompletionParamType.TOP_P,
            CompletionParamType.ON_STREAM,
            CompletionParamType.MAX_GENERATED_TOKENS
        ]

    def on_generate(self, text: str, params: CompletionParams) -> str:
        completion = openai.Completion.create(
            engine=self.model,
            prompt=text,
            max_tokens=params.max_generated_tokens,
            temperature=params.temperature,
            top_p=params.top_p,
            stream=True,  # Prefer stream to speed up.
            stop=params.stop_string,
            n=1,
        )
        full_text = ""
        for c in completion:
            try:
                streamtext = c["choices"][0]["text"]
                full_text += streamtext
            except:
                raise RuntimeError(c)
            
            len_text = len(tokenizer.tokenize(full_text))
            
            if params.stop_string in full_text:
                full_text = full_text.split(params.stop_string)[0]
                break
            if len_text >= params.max_generated_tokens:
                break
            if params.on_stream is not None:
                if not params.on_stream(streamtext):
                    break
        
        return full_text