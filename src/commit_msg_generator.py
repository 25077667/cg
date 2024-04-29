"""
Commit Message Generator

This module provides functionality for generating commit messages using the OpenAI API.
"""

from random import shuffle
from typing import Generator
import re
import requests

from .config_parser import Config
from .git_diff import git_diff


class TokenManager:
    """
    A singleton class to manage API tokens.
    """

    _instance = None

    @classmethod
    def get_instance(cls, tokens: list[str]):
        if cls._instance is None:
            cls._instance = cls(tokens)
        return cls._instance

    def __init__(self, tokens: list[str]):
        if not tokens:
            raise ValueError("Token list must not be empty.")
        self._constant_pool = tuple(tokens)
        self._access_pool = list(self._constant_pool)
        shuffle(self._access_pool)

    def pop_token(self):
        if not self._access_pool:
            self._access_pool = list(self._constant_pool)
            shuffle(self._access_pool)
        return self._access_pool.pop(0)


def make_api_request(config: Config, messages: list[dict], token: str) -> dict:
    """
    Makes an API request to the OpenAI chat completions endpoint.

    Args:
        config (Config): The configuration object containing model settings.
        messages (list[dict]): The list of messages to include in the API request.
        token (str): The API token for authentication.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"}
    data = {
        "model": config["model"],
        "messages": messages,
        "max_tokens": config["max_tokens"],
        "temperature": config["temperature"],
        "top_p": config["top_p"],
        "frequency_penalty": config["frequency_penalty"],
        "presence_penalty": config["presence_penalty"],
    }
    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=config["timeout"])
    response.raise_for_status()
    return response.json()


def generate_commit_message(
    config: Config, repo_path: str
) -> Generator[str, None, None]:
    """
    Generates commit messages based on the provided configuration and repository path.

    Args:
        config (Config): The configuration object containing the necessary settings.
        repo_path (str): The path to the repository.

    Yields:
        str: A commit message generated based on the configuration and repository changes.
             empty string if no message is generated.
    """
    diff = git_diff(repo_path)
    if not diff:
        return

    token_manager = TokenManager.get_instance(config["tokens"])
    system_prompt = config["system_prompt"]

    while True:
        token = token_manager.pop_token()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diff},
        ]
        result = make_api_request(config, messages, token)
        commit_msg = result["choices"][0]["message"]["content"]

        if (
            commit_msg
            and get_score(config, diff, commit_msg) >= config["revise"]["threshold"]
        ):
            yield commit_msg


def get_score(config: Config, diff: str, msg: str) -> float:
    """
    Calculate the quality score of the commit message.
    """
    messages = [
        {"role": "system", "content": config["revise"]["prompt"]},
        {"role": "user", "content": f"Source diff:\n{
            diff}\n\nCommit message:\n{msg}"},
    ]
    token_manager = TokenManager.get_instance(config["tokens"])
    result = make_api_request(config, messages, token_manager.pop_token())
    return extract_score(result)


def extract_score(result: dict) -> float:
    """
    Extracts the score from the API response.

    Args:
        result (dict): The JSON response from the API.

    Returns:
        float: The extracted score.

    Raises:
        ValueError: If the score cannot be extracted.
    """
    content = result["choices"][0]["message"]["content"]
    match = re.search(r"(\d+\.\d+)", content)
    if match:
        return float(match.group(1))

    print(f"failed to extract score from: {content}")
    return 0.0  # default to 0 if score cannot be extracted
