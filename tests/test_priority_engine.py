import random
import time 
from easytextgen import EasyPrompt
from easytextgen.engine.base import TextGenerationEngine, CompletionParams
from easytextgen.engine import PriorityEngine


class EngineWithId(TextGenerationEngine):
    def __init__(self, engine_id: str) -> None:
        self.engine_id = engine_id


class AlwaysErrorEngine(EngineWithId):
    def on_generate(self, text: str, params: CompletionParams) -> str:
        raise Exception("AlwaysErrorEngine is designed to be always error!")


class AlwaysSuccessEngine(EngineWithId):
    def on_generate(self, text: str, params: CompletionParams) -> str:
        return "AlwaysSuccessEngine is designed to be always success!"


class UncertainEngine(EngineWithId):
    def on_generate(self, text: str, params: CompletionParams) -> str:
        randnum = random.randint(0, 10)
        if randnum > 5:
            return "UncertainEngine returned success"
        raise Exception("UncertainEngine returned error")


class EngineWithLimits(EngineWithId):
    def __init__(self, engine_id: str, init_usages: int = 1) -> None:
        super().__init__(engine_id)
        self.usage_left = init_usages
    
    def on_generate(self, text: str, params: CompletionParams) -> str:
        if self.usage_left > 0:
            self.usage_left -= 1
            return "Success"
        
        raise Exception("No more usages!")


def test_priority_fake_error_then_use_always_success():
    ep = EasyPrompt.from_file("./.easyprompts/test/empty-priority")
    ep.engine = PriorityEngine(reset_every_secs=1, engines=[
        AlwaysErrorEngine("always_error"),
        AlwaysSuccessEngine("always_success"),
    ])
    out1 = ep.get_output("Just arbitrary text")
    assert "AlwaysSuccessEngine" in out1.extras["info"]["engine"]


def test_reset_priority_after_1_sec():
    ep = EasyPrompt.from_file("./.easyprompts/test/empty-priority")
    ep.engine = PriorityEngine(reset_every_secs=1, engines=[
        EngineWithLimits("with_limits"),
        AlwaysSuccessEngine("always_success"),
    ])
    
    # Expected: Use EngineWithLimits because it has 1 quota.
    out = ep.get_output("Just arbitrary text")
    assert "EngineWithLimits" in out.extras["info"]["engine"]

    # Expected: LimitError then jump to AlwaysSuccess. EngineWithLimits quota resets to 1.
    out = ep.get_output("Just arbitrary text")
    assert "AlwaysSuccessEngine" in out.extras["info"]["engine"]
    
    # Expected: Still use AlwayasSuccess because hasn't 1 sec yet
    out = ep.get_output("Just arbitrary text")
    assert "AlwaysSuccessEngine" in out.extras["info"]["engine"]
    
    time.sleep(1)
    
    # Expected: Use EngineWithLimits with it's 1 quota.
    out = ep.get_output("Just arbitrary text")
    assert "EngineWithLimits" in out.extras["info"]["engine"]
