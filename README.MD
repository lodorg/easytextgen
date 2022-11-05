# easytextgen

Features:
- Interface to 3rd party text generation services such as OpenAI, TextSynth, or EleutherAI.
- Define your own custom text generation engine.
- Create your own prompts with EasyPrompt.
- Text streaming is supported (if the 3rd party service text streaming is available).

TODO:
- Create tests
- Pypi listing
- Prompt override (in the easyprompt file, ability to override default prompt when using different engine)

## Installation

Pypi
```
Coming Soon!
```

GitHub
```
pip install git+https://github.com/lodorg/easytextgen
```

Local
```
git clone https://github.com/lodorg/easytextgen
cd easytextgen
pip install -e .
```

## Basic Usage

### Using Text Generation Engine

```python
from easytextgen import CompletionParams
from easytextgen.engine import EleutherEngine

engine = EleutherEngine(model="GPT-J-6B")
params = CompletionParams(input_text="My name is John and I like to", temperature=0.9)
result = engine.generate(params)
print(result.output_text)
```

### Using EasyPrompt

Example EasyPrompt with Single Argument

```python
from easytextgen import EasyPrompt

prompt = EasyPrompt.from_file("./easyprompts/tweet-sentiment")  # Path to yaml file
result = prompt.get_output("This product is awful. Not buying this again.")
print(result.output_text)
```

Example EasyPrompt with Multiple Arguments (Use Keyword Arguments)

```python
from easytextgen import EasyPrompt

prompt = EasyPrompt.from_file("./easyprompts/style-changer")
result = prompt.get_output(text="I need to meet ur daddy ASAP!", style="Formal")
print(result.output_text)
```

### Create New EasyPrompt

```yaml
engine:
  name: "EleutherEngine"
  model: "GPT-J-6B"
      
stop_string: "\n"
temperature: 0.11
top_p: 1.0
top_k: 40
max_generated_tokens: 32
seed: 0
force_safety: false
on_stream: null
prompt: |
  This is a tweet sentiment classifier

  Tweet: "I loved the new Batman movie!"
  Sentiment: Positive
  ###
  Tweet: "I hate it when my phone battery dies."
  Sentiment: Negative
  ###
  Tweet: "My day has been good!"
  Sentiment: Positive
  ###
  Tweet: "This is the link to the article"
  Sentiment: Neutral
  ###
  Tweet: "{{text}}"
  Sentiment:
```
