from abc import ABC, abstractmethod
from dataclasses import dataclass
from os import PathLike
from copy import deepcopy
from typing import Union
import os
import yaml

from easytextgen.prompt_utils import get_engine, get_prompt_variables, get_variables, set_variables
from easytextgen.completion import CompletionParams, CompletionResult
from easytextgen.engine import TextGenerationEngine


@dataclass
class EasyPrompt:
    """Generic prompt type for auto prompting. Parameter style. Feel free to import and use `prompt_utils` """
    prompt: str
    engine: TextGenerationEngine
    parameters: CompletionParams
    
    @staticmethod
    def from_file(path: Union[PathLike, str]) -> "EasyPrompt":
        path_string = str(path).replace(".yml", "").replace(".yaml", "")
        file_exist = False

        for ext in [".yml", ".yaml"]:
            if os.path.exists(path_string + ext):
                with open(path_string + ext, "r") as fs:
                    params = yaml.safe_load(fs)
                    prompt = params["prompt"]
                    file_exist = True
                    break
        
        if not file_exist:
            raise FileNotFoundError(f"File not found `{path_string}` (.yml/.yaml)")
            
        engine = get_engine(params["engine"])
        gen_params = CompletionParams(input_text="", **params)
        return EasyPrompt(prompt=prompt, engine=engine, parameters=gen_params)
    
    def get_prompt_variables(self) -> list:
        return get_prompt_variables(self.prompt)
    
    def get_output(self, *args, **kwargs) -> CompletionResult:
        args_in = kwargs.copy()
        
        prompt = deepcopy(self.prompt)
        variables = get_variables(prompt)
        
        for kwarg in args_in.keys():
            if kwarg not in variables:
                raise Exception(f"Variable `{kwarg}` is not in prompt variables. "
                                f"Here are the list of variables: {self.get_prompt_variables()}")
        
        if len(variables) == 1 and len(args) == 1:
            args_in = {variables[0]: args[0]}
        
        prompt = set_variables(prompt, **args_in)
        
        params = self.parameters.copy()
        params.input_text = prompt
        
        output = self.engine.generate(params)
        output.extras["autoprompt"] = {
            "prompt": self.prompt,
            "arguments": args_in
        }
        return output


class AutoPromptAbstract(ABC, EasyPrompt):
    """Generic prompt type for auto prompting. Abstract style. Feel free to import and use `prompt_utils` """
    
    def __init__(self) -> None:
        self.prompt: str = self.define_prompt()
        self.generator: TextGenerationEngine = self.define_engine()
        self.parameters: CompletionParams = self.define_parameters()
        
    @abstractmethod
    def define_prompt(self) -> str:
        raise NotImplementedError() 
        
    @abstractmethod
    def define_engine(self) -> TextGenerationEngine:
        raise NotImplementedError()
    
    @abstractmethod
    def define_parameters(self) -> CompletionParams:
        raise NotImplementedError()
    