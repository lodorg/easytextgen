from rich import print
from typing import Optional, Callable, TYPE_CHECKING
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


# Enable VSCode Intellisense for Pydantic models
if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    def dataclass(model):
        return model


@dataclass
class CompletionParams(BaseModel):
    """ Text completion parameters.
    ```
    input_text: str
    top_p: float = 1.0
    top_k: int = 40
    temperature: float = 0.75
    presence_penalty: float = 0
    frequency_penalty: float = 0
    seed: int = 0 (Zero means regenerate seed number every request)
    max_generated_tokens: int = 32
    stop_string: str = "<|endoftext|>"
    force_safety: bool = False
    on_stream: Optional[Callable[[str], bool]] = None
    ```
    Example `on_stream` callback:
    ```
    def sample_on_stream(text: str) -> bool:
        ui_text = "previous_text + current_text"
        return True  # Continue streaming text?
    ```
    """
    input_text: str
    top_p: float = 1.0
    top_k: int = 40
    temperature: float = 0.75
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    repetition_penalty: float = 1.0
    seed: int = 0
    max_generated_tokens: int = 32
    stop_string: str = "<|endoftext|>"
    force_safety: bool = False
    on_stream: Optional[Callable[[str], bool]] = None


@dataclass
class CompletionResult(BaseModel):
    input_text: str
    output_text: str
    extras: dict