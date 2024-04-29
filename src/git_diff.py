"""
This module provides a function for generating git diff for added files and the head commit.
"""

from git import Repo


def git_diff(repo_path: str) -> str:
    """
    Generate git diff for added files and the head commit in a Git repository.

    Args:
        repo_path (str): The path to the Git repository.

    Returns:
        str: The git diff as a string.
    """
    repo = Repo(repo_path)
    return repo.git.diff("HEAD")
