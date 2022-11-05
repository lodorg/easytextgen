```yaml
engine:
  name: "PriorityEngine"
  engines:
    - name: "EleutherEngine"
      model: "GPT-J-6B"
      
stop_string: "\n"
temperature: 0.11
top_p: 1.0
top_k: 40
max_generated_tokens: 32
seed: 0
force_safety: false
on_stream: null
```
```txt
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