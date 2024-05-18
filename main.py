"""
Main Python File
"""

import os
import sys
import tempfile
import subprocess
from git import Repo, Actor, InvalidGitRepositoryError, NoSuchPathError

from src.args import args
from src.config_parser import Config
from src.commit_msg_generator import generate_commit_message


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

    raise RuntimeError(
        "Error: No git repository found in the current directory or any parent directories."
    )


def get_user_input(prompt: str, default: str) -> str:
    """
    Prompt the user for input and return the input value or the default value.
    """
    user_input = input(f"{prompt} ({default}) ").strip()
    if not user_input:
        return default
    return user_input


def check_git_config(repo: Repo):
    """
    Check if the necessary git configuration is set (user.name, user.email, and SSH key).
    Emit alerts if any configuration is missing.
    """
    config_reader = repo.config_reader()
    missing_configs = []

    try:
        author = config_reader.get_value("user", "name")
    except (KeyError, ValueError):
        missing_configs.append("user.name")

    try:
        author_email = config_reader.get_value("user", "email")
    except (KeyError, ValueError):
        missing_configs.append("user.email")

    if missing_configs:
        print(f"Alert: Missing Git configuration: {', '.join(missing_configs)}")
        print("Please set them using the following commands:")
        if "user.name" in missing_configs:
            print("  git config --global user.name 'Your Name'")
        if "user.email" in missing_configs:
            print("  git config --global user.email 'your.email@example.com'")

    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa")
    if not os.path.exists(ssh_key_path):
        print("Alert: SSH key not found.")
        print(
            "Please generate one using the following command and add it to your SSH agent and GitHub account:"
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
    except Exception as e:
        print(f"Error: Failed to commit the message. Details: {e}")
        sys.exit(1)


def edit_message(orig: str) -> str:
    """
    Edit the commit message in the editor specified by the EDITOR environment variable.
    """
    editor = os.environ.get("EDITOR", "vim")
    with tempfile.NamedTemporaryFile(suffix=".tmp") as temp_file:
        temp_file.write(orig.encode())
        temp_file.flush()
        subprocess.call([editor, temp_file.name])

        temp_file.seek(0)
        # With open it and read it for result returning
        with open(temp_file.name, "r", encoding="utf-8") as tmp_file:
            return tmp_file.read()


def get_commit_message(repo_path: str) -> str:
    """
    Generate commit messages based on the configuration and prompt the user for confirmation.
    Return the selected commit message or an empty string if none is selected.
    """
    try:
        config_path = args["config"]
        config = Config(config_path)

        for msg in generate_commit_message(config, repo_path):
            print(msg)
            if config["interactive"]:
                user_selection = get_user_input(
                    "Is this commit message satisfactory? (Y/n/e)", "Y"
                )
                if user_selection.lower() == "y":
                    return msg
                if user_selection.lower() == "n":
                    continue
                if user_selection.lower() == "e":
                    return edit_message(msg)
            else:
                return msg

        return ""
    except Exception as e:
        print(f"Error: Failed to generate commit message. Details: {e}")
        sys.exit(1)


def main() -> None:
    """
    Main function that generates and commits a message based on the configuration.
    """
    try:
        repo_path = get_repo_path(os.getcwd())
        commit_message = get_commit_message(repo_path)
        if commit_message:
            commit_hash = commit_full_text_message(repo_path, commit_message)
            print(f"Commit message generated and committed: {commit_hash}")
        else:
            print("No commit message generated. Exiting...")
            sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred. Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
