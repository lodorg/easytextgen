import string
import time
from abc import ABC, abstractmethod

from easytextgen.completion import CompletionParams, CompletionResult


class TextGenerationEngine(ABC):
    
    @abstractmethod
    def on_generate(self, text: str, params: CompletionParams) -> str:
        raise NotImplementedError()

    def get_available_parameters(self) -> list[str]:
        return ["stop_string"]
    
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
        
        # Must return the completed text only
        result = self.on_generate(sanitized_text, params)  # type: ignore
        result = result.replace(sanitized_text, "", 1)
        result = result.split(params.stop_string)[0]
        
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
        
        result = CompletionResult(input_text=sanitized_text, output_text=result, extras=extras)        
        return result