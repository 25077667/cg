import json
import os

# Get environment variables of GPT_TOKENS
# Split the string by comma or semicolon
GPT_TOKENS = tuple(os.environ.get(
    'GPT_TOKENS', '').replace(
    ';', ',').replace(
    ':', ',').split(
    ',')
)

DEFAULT_CONFIG = {
    "tokens": list(GPT_TOKENS),
    "interactive": True,
    "model": "gpt-3.5-turbo",
    "system_prompt":
    """I want you to act as a commit message generator. I will provide you with the git diff, and you should generate an appropriate commit message using the conventional commit format.

Write git commit message following these rules:
1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line and use imperatives
4. Do not end the subject line with a period
5. Wrap the body at 72 characters
6. Use the body to explain what, why and how
7. Only writes what was changed
    """,
    "temperature": 0.35,
    "top_p": 0.7,
    "max_tokens": 256,
    "frequency_penalty": 1.6,
    "presence_penalty": 0.1,
}


class Config:
    def __init__(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                self.json_file = json.load(f)
        except FileNotFoundError:
            # create the directory if it does not exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # create the file if it does not exist
            with open(path, 'w') as f:
                json.dump(DEFAULT_CONFIG, f)
            self.json_file = DEFAULT_CONFIG.copy()

    def __getitem__(self, key: str):
        return self.json_file[key]
