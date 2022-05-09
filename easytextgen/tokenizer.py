def tokenize(text: str) -> list[int]:
    """Dummy tokenizer that only used to approximate number of tokens."""
    length = int(len(text) / 4)
    lst = []
    for _ in range(length):
        lst.append(0)
    return lst
    
# tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
