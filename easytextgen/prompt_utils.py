from logging import warn
import re
import warnings


prefix = "{{"
postfix = "}}"


def get_variables(text: str) -> list:
    """Extract variables from prompt like this:
    {{name}}:{{message}} would returns ['name', 'message']
    """
    variables = []
    for var in re.findall(f"{prefix}(.*?){postfix}", text):
        if var not in variables:
            variables.append(var)
    return variables


def set_variables(_text: str, **kwargs) -> str:
    """Replaces variable matched pattern in text. Use kwargs to define the variables."""
    
    variables = get_variables(_text)
    prompt_string = _text + ""
    
    for var in variables:
        if var not in kwargs.keys():
            raise ValueError(f"Variable `{var}` not assigned. This prompt uses: `{variables}`.")
        prompt_string = prompt_string.replace(prefix + var + postfix, kwargs[var])
    
    for key in kwargs.keys():
        if key not in variables:
            warnings.warn(f"Supplied variable `{key}` is not in text!")
    
    return prompt_string


def get_prompt_variables(path: str) -> list:
    """Get a list of variables from a prompt"""
    
    with open(path, "r") as fs:
        prompt_string = fs.read()
    
    return get_variables(prompt_string)


def load_prompt(_path: str, **kwargs) -> str:
    """Replaces variable matched pattern in prompt. Use kwargs to define the variables."""
    
    with open(_path, "r") as fs:
        prompt_string = fs.read()
    
    return set_variables(prompt_string, **kwargs)
    
    
def get_engine(params: dict):
    """
    Converts dict into TextGenerationEngine instance
    Example: 
    ```
    {
        "name": "PriorityEngine",
        "engines": [
            {"name": "Engine1", "api_key": "123"},
            {"name": "Engine2", "api_key": "12345"},
        ]
    }
    ```
    Converts following Python code using 'getattr'
    ```
    engine = PriorityEngine(engines=[
        Engine1(api_key="123"),
        Engine2(api_key="12345")
    ])
    ```
    """
    from easytextgen import engine

    name = params.pop("name")
    engine_class = getattr(engine, name)
    
    if "engines" in params:
        params["engines"] = [get_engine(engine) for engine in params["engines"]]
        
    return engine_class(**params)