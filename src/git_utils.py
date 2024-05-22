"""
A helper module for git-related operations.
"""

import os
import sys
from logging import getLogger
from git import Repo, Actor, InvalidGitRepositoryError, NoSuchPathError

logger = getLogger(__name__)


class GitConfigError(Exception):
    """Custom exception for git configuration errors"""

    def __init__(self, message: str):
        super().__init__(message)


def get_repo_path(start_path: str) -> str:
    """
    Traverse from the start_path to the top-level directory to find a git repository.
    Prioritize submodules by using the first repository found from the current directory upwards.

    Args:
        start_path (str): The starting directory path.

    Returns:
        str: The path to the git repository.
    """
    current_path = start_path
    while True:
        try:
            repo = Repo(current_path, search_parent_directories=True)
            return repo.git.rev_parse("--show-toplevel")
        except (InvalidGitRepositoryError, NoSuchPathError):
            # Move to the parent directory
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:  # Reached the top level
                break
            current_path = parent_path

    raise GitConfigError(
        "Error: No git repository found in the current directory or any parent directories."
    )


def check_git_config(repo: Repo):
    """
    Check if the necessary git configuration is set (user.name, user.email, and SSH key).
    Emit alerts if any configuration is missing.
    """
    config_reader = repo.config_reader()
    missing_configs = []

    try:
        _ = config_reader.get_value("user", "name")
    except (KeyError, ValueError):
        missing_configs.append("user.name")

    try:
        _ = config_reader.get_value("user", "email")
    except (KeyError, ValueError):
        missing_configs.append("user.email")

    if missing_configs:
        logger.warning("Missing Git configuration: %s", ", ".join(missing_configs))
        print("Please set them using the following commands:")
        if "user.name" in missing_configs:
            print("  git config --global user.name 'Your Name'")
        if "user.email" in missing_configs:
            print("  git config --global user.email 'your.email@example.com'")

    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    if not os.path.exists(ssh_key_path):
        logger.warning("SSH key not found.")
        print(
            "Please generate one using the following command and add it to "
            + "your SSH agent and GitHub account:"
        )
        print("  ssh-keygen -t rsa -b 4096 -C 'your.email@example.com'")


def commit_full_text_message(repo_path: str, message: str) -> str:
    """
    Commit the provided message to the repository at the given path and return the commit hash.
    """
    try:
        repo = Repo(repo_path)
        check_git_config(repo)

        author = str(repo.config_reader().get_value("user", "name"))
        author_email = str(repo.config_reader().get_value("user", "email"))
        committer = Actor(author, author_email)

        return repo.index.commit(message=message, committer=committer).hexsha
    except Exception as exception_detail:  # pylint: disable=broad-except
        logger.error("Failed to commit the message. Details: %s", exception_detail)
        sys.exit(1)


def get_git_editor() -> str:
    """
    Get the configured git editor or use 'vim' as the default.
    """
    editor = os.getenv("GIT_EDITOR", os.getenv("EDITOR"))
    if editor is None:
        if sys.platform.startswith("win"):
            editor = "notepad.exe"
        else:
            editor = "vim"
    return editor
