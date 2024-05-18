"""
Configuration parser for the commit message generator.
"""

import json
import os

GPT_TOKENS = tuple(
    os.environ.get("GPT_TOKENS", "").replace(";", ",").replace(":", ",").split(",")
)

DEFAULT_CONFIG = {
    "tokens": list(GPT_TOKENS),
    "interactive": True,
    "model": "gpt-3.5-turbo",
    "system_prompt": """I want you to act as a commit message generator.
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
        "threshold": 6.5,
        "max_tokens": 128,
        "temperature": 1,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "prompt": """You are a scoring machine, just output the score of
the git commit message is suitable. You should only output a number
from 0.0 to 10.0, without any reason.
""",
    },
    "timeout": 30,
}


def init_first_token() -> str:
    """
    Only when the user is using cg at the first time and they didn't give it any token,
    this function will be called to require the first token from the user.

    Returns:
        str: The first token.
    """
    print(
        "It seems that you are using cg at the first time, please provide a token for cg."
    )
    print("You can get a token from https://beta.openai.com/account/api-keys")
    print("Please note that you should use the secret key, not the publishable key.")
    print(
        "If you don't have a secret key, you can create one by clicking the"
        + "'Create new API key' button."
    )
    print("After you get the token, please paste it here:")
    token = input()
    # The token must contains "sk-" prefix.
    if not token.startswith("sk-"):
        print("The token is invalid, please try again.")
        return init_first_token()
    return token


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
        self.path = path
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.json_file = json.load(file)
        except FileNotFoundError:
            self.json_file = DEFAULT_CONFIG.copy()
            if self.json_file["tokens"] == [""]:
                self.json_file["tokens"] = [init_first_token()]
            self._save_config()
        self._ensure_defaults()

    def __getitem__(self, key: str):
        """
        Get the value associated with the given key.

        Args:
            key (str): The key for accessing the value.

        Returns:
            Any: The value associated with the key.
        """
        return self.json_file[key]

    def __setitem__(self, key: str, value: str) -> None:
        """
        Set the value associated with the given key.

        Args:
            key (str): The key for accessing the value.
            value (str): The value to be set.
        """
        self.json_file[key] = value
        self._save_config()

    def _ensure_defaults(self):
        """
        Ensure all default keys are present in the JSON file and update if necessary.
        """
        updated = False
        for key, value in DEFAULT_CONFIG.items():
            if key not in self.json_file:
                self.json_file[key] = value
                updated = True
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if sub_key not in self.json_file[key]:
                        self.json_file[key][sub_key] = sub_value
                        updated = True
        if updated:
            self._save_config()

    def _save_config(self):
        """
        Save the current configuration to disk.
        """
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.json_file, file, indent=4)


# Example usage:
# config = Config("/path/to/config.json")
# print(config["model"])
# config["model"] = "new-model"
