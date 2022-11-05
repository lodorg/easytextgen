import json
import attr
import requests
from easytextgen import tokenizer
from easytextgen.completion import CompletionParams
from easytextgen.engine.base import CompletionParamType, TextGenerationEngine


class TextsynthEngine(TextGenerationEngine):
    """ https://textsynth.com. """

    models: list[str] = ["gptj_6B", "boris_6B", "fairseq_gpt_13B", "gptneox_20B"]

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def get_available_parameters(self) -> list:
        return super().get_available_parameters() + [
            CompletionParamType.TEMPERATURE,
            CompletionParamType.TOP_K,
            CompletionParamType.TOP_P,
            CompletionParamType.SEED,
            CompletionParamType.ON_STREAM,
            CompletionParamType.MAX_GENERATED_TOKENS,
            CompletionParamType.PRESENCE_PENALTY,
            CompletionParamType.FREQUENCY_PENALTY,
        ]
    
    def on_generate(self, text: str, params: CompletionParams) -> str:
        request_parameters = json.dumps({
            "prompt": text,
            "temperature": params.temperature,
            "top_k": params.top_k,
            "top_p": params.top_p,
            "presence_penalty": params.presence_penalty,
            "frequency_penalty": params.frequency_penalty,
            "seed": params.seed,
            "stream": True,
        })
        return self._request_completion(params, request_parameters)
    
    def _request_completion(self, params: CompletionParams, req_params) -> str:
        full_text: str = ""
        url = f"https://api.textsynth.com/v1/engines/{self.model}/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        with requests.request("POST", url, data=req_params, headers=headers, stream=True) as resp:
            
            for r in resp.iter_lines():
                stream = str(r, encoding="utf-8")
                
                if len(stream) < 3:
                    continue
                
                resp_dict = json.loads(stream)
                
                if "text" not in resp_dict.keys():
                    raise RuntimeError(resp_dict)
                
                streamtext = resp_dict["text"]
                full_text += streamtext
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