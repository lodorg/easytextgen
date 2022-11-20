from easytextgen import EasyPrompt
import yaml


def test_easyprompt_from_file_md():
    prompt = EasyPrompt.from_file("./.easyprompts/test/tweet-sentiment-md")
    result = prompt.get_output("This product is awful. Not buying this again.").output_text.lower()
    assert "negative" in result


def test_easyprompt_from_file_yml():
    prompt = EasyPrompt.from_file("./.easyprompts/test/tweet-sentiment-yml")
    result = prompt.get_output("This product is awful. Not buying this again.").output_text.lower()
    assert "negative" in result


def test_easyprompt_from_string_md():
    prompt_str = open("./.easyprompts/test/tweet-sentiment-md.md", "r").read()
    prompt = EasyPrompt.from_string(prompt_str)
    result = prompt.get_output("This product is awful. Not buying this again.").output_text.lower()
    assert "negative" in result


def test_easyprompt_from_string_yml():
    prompt_str = open("./.easyprompts/test/tweet-sentiment-yml.yml", "r").read()
    prompt = EasyPrompt.from_string(prompt_str)
    result = prompt.get_output("This product is awful. Not buying this again.").output_text.lower()
    assert "negative" in result
