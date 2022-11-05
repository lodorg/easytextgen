from easytextgen.completion import CompletionParams
from easytextgen.engine.base import TextGenerationEngine
from easytextgen.priority import Priority


class PriorityEngine(TextGenerationEngine):
    """
    Uses engine prioritized by list order.
    If one of the engines error, move to the next engine.
    The working engine will be prioritized into the top of the order.
    """
    
    def __init__(self, engines: list[TextGenerationEngine]) -> None:
        self.engines = engines
        self.priority = Priority(self.engines)
      
    def get_available_parameters(self) -> list:
        return self.priority.get_first().get_available_parameters()
        
    def get_info(self, params: CompletionParams) -> dict:
        engine: TextGenerationEngine = self.priority.get_first()
        info = super().get_info(params)
        info["available_parameters"] = engine.get_available_parameters()
        info["engine"] = f"{type(self).__name__}:{type(engine).__name__}"
        info["model"] = getattr(engine, "model", None)
        return info

    def on_generate(self, text: str, params: CompletionParams) -> str:
        for engine in self.priority.items:
            try:
                engine: TextGenerationEngine
                out = engine.on_generate(text, params)
                self.priority.move_first(engine)
                return out
            except Exception as e:
                print(f"[ERROR at Engine '{engine}']: {e}")
                raise Exception("All engines failure.")