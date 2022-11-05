import string
import time
import random
from abc import ABC, abstractmethod

from easytextgen.completion import CompletionParams, CompletionResult


class CompletionParamType:
    TEMPERATURE = "temperature"
    TOP_P = "top_p"
    TOP_K = "top_k"
    MAX_GENERATED_TOKENS = "max_generated_tokens"
    REPETITION_PENALTY = "repetition_penalty"
    PRESENCE_PENALTY = "presence_penalty"
    FREQUENCY_PENALTY = "frequency_penalty"
    STOP_STRING = "stop_string"
    SEED = "seed"
    ON_STREAM = "on_stream"
    

class TextGenerationEngine(ABC):
    
    @abstractmethod
    def on_generate(self, text: str, params: CompletionParams) -> str:
        raise NotImplementedError()

    def get_available_parameters(self) -> list[str]:
        return [CompletionParamType.STOP_STRING]
    
    def get_info(self, params: CompletionParams) -> dict:
        return {
            "engine": f"{type(self).__name__}",
            "model": getattr(self, "model", None),
            "available_parameters": self.get_available_parameters(),
            "current_parameters": params.__dict__,
        }
    
    def generate(self, params: CompletionParams, *args, **kwargs) -> CompletionResult:
        input_timestamp = int(time.time() * 1000)
        
        # Sanitize input text
        printable = set(string.printable)
        sanitized_text = "".join(filter(lambda x: x in printable, params.input_text))
        if len(sanitized_text) <= 1:
            raise ValueError("Length of input can't be zero.")
        
        # If seed is zero, randomize seed
        if params.seed == 0:
            params.seed = (int(time.time()) % 1000000) + random.randrange(1, 1000000)
        
        # Must return the completed text only
        output_text = self.on_generate(sanitized_text, params)  # type: ignore
        output_text = output_text.replace(sanitized_text, "", 1)
        output_text = output_text.split(params.stop_string)[0]
        
        # TODO: Add a safety filter layer
        output_timestamp = int(time.time() * 1000)
        extras = {
            "info": self.get_info(params),
            "safety": {},
            "timestamp_in": input_timestamp,
            "timestamp_out": output_timestamp,
            "latency": output_timestamp - input_timestamp,
        }
        
        # TODO: Result = message regarding safety if params.force_safety = True
        
        result = CompletionResult(input_text=sanitized_text, output_text=output_text, extras=extras)        
        return result