"""
Configuration parser for the commit message generator.
"""
import json
import os

GPT_TOKENS = tuple(os.environ.get('GPT_TOKENS', '').replace(
    ';', ',').replace(':', ',').split(','))

DEFAULT_CONFIG = {
    "tokens": list(GPT_TOKENS),
    "interactive": True,
    "model": "gpt-3.5-turbo",
    "system_prompt":
    """I want you to act as a commit message generator.
I will provide you with the git diff, and you should generate
an appropriate commit message using the conventional commit format.

Write git commit message following these rules:
1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line and use imperatives
4. Do not end the subject line with a period
5. Wrap the body at 72 characters
6. Use the body to explain what, why, and how
7. Only write what was changed
    """,
    "temperature": 0.35,
    "top_p": 0.7,
    "max_tokens": 256,
    "frequency_penalty": 1.6,
    "presence_penalty": 0.1,
    "revise": {
        "model": "gpt-3.5-turbo",
        "threshold": 0.6,
        "prompt": """You are a scoring machine, just output the score of
the git commit message is suitable. You should only output a number
from 0.0 to 10.0, without any reason.
"""
    },
}


class Config:
    """
    A class for managing configuration settings.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize the Config instance.

        Args:
            path (str): The path to the JSON configuration file.
        """
        try:
            with open(path, 'r', encoding='utf-8') as file:
                self.json_file = json.load(file)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(DEFAULT_CONFIG, file)
            self.json_file = DEFAULT_CONFIG.copy()

    def __getitem__(self, key: str):
        """
        Get the value associated with the given key.

        Args:
            key (str): The key for accessing the value.

        Returns:
            Any: The value associated with the key.
        """
        return self.json_file[key]

    # Dummy function for pylint
    def __setitem__(self, key: str, value: str) -> None:
        """
        Set the value associated with the given key.

        Args:
            key (str): The key for accessing the value.
            value (str): The value to be set.
        """
        self.json_file[key] = value
