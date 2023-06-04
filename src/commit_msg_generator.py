from random import shuffle
import requests
from typing import Generator

from .config_parser import Config
from .git_diff import git_diff


class Unused_token:
    _instance = None
    constant_pool = tuple()
    access_pool = []

    def __new__(cls, string_list: list[str]):
        # Check if the string_list is empty, then raise an error
        if len(string_list) == 0:
            raise ValueError(
                'tokens should not be empty.\n ' +
                'Please set the environment variable GPT_TOKENS to a non-empty string.\n ' +
                '\t For example export GPT_TOKENS="token1,token2,token3"\n' +
                'Or edit the config file to set the tokens.')
        if not cls._instance:
            cls._instance = super(Unused_token, cls).__new__(cls)
            cls._instance.constant_pool = tuple(*string_list)
            cls._instance.access_pool = list(*cls._instance.constant_pool)
            shuffle(cls._instance.access_pool)
        return cls._instance

    def copy_pool(self) -> None:
        self.access_pool = list(*self.constant_pool)

    def pop(self) -> str:
        if len(self.access_pool) == 0:
            self.copy_pool()
            shuffle(self.access_pool)
        return self.access_pool.pop(0)


# yield string of the commit message result
# Keep generating until the user is satisfied
def generate_commit_message(
        config: Config, repo_path: str) -> Generator[str, None, None]:
    unused_token = Unused_token(config['tokens'])

    message = [
        {
            "role": "system",
            "content": config['system_prompt'],
        },
        {
            "role": "user",
            "content": git_diff(repo_path),
        },
    ]

    data = {
        'model': config['model'],
        'messages': message,
        'max_tokens': config['max_tokens'],
        'temperature': config['temperature'],
        'top_p': config['top_p'],
        'frequency_penalty': config['frequency_penalty'],
        'presence_penalty': config['presence_penalty'],
    }

    while config['interactive'] is True:
        #! We don't use OpenAI Python API because we don't want to couple it with our code.
        #! For hacking purposes, we use requests library to send HTTP request to OpenAI API.
        #! We need to poll the tokens to avoid rate limit.

        # Link reference: https://platform.openai.com/docs/api-reference/chat/create
        # Request from OpenAI API like:
        # curl https://api.openai.com/v1/chat/completions \
        #   -H "Content-Type: application/json" \
        #   -H "Authorization: Bearer $OPENAI_API_KEY" \
        #   -d '{
        #     "model": "gpt-3.5-turbo",
        #     "messages": [{"role": "user", "content": "Hello!"}]
        #     "max_tokens": 5,
        #     "temperature": 0.9,
        #   }'

        api_key = unused_token.pop()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        }

        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
        )

        # Response from OpenAI API like:
        # {
        #   "id": "scc-123",
        #   "object": "chat.completion",
        #   "created": 1619795811,
        #   "choices": [{
        #     "index": 0,
        #     "message": {
        #       "role": "assistant",
        #       "content": "\n\nHello there, how may I assist you today?",
        #     },
        #     "finish_reason": "stop"
        #   }],
        #   "usage": {
        #     "prompt_tokens": 9,
        #     "completion_tokens": 12,
        #     "total_tokens": 21
        #   }
        # }

        # Yield the first choice
        yield response.json()['choices'][0]['text']
