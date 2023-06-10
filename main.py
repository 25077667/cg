"""
Main Python File
"""
import os
import sys
import tempfile
import subprocess
from git import Repo, Actor

from src.args import args
from src.config_parser import Config
from src.commit_msg_generator import generate_commit_message

CURRENT_PATH = os.path.curdir


def get_user_input(prompt: str, default: str) -> str:
    """
    Prompt the user for input and return the input value or the default value.
    """
    user_input = input(f"{prompt} ({default})")
    if not user_input:
        return default
    return user_input


def commit_full_text_message(repo_path: str, message: str) -> str:
    """
    Commit the provided message to the repository at the given path and return the commit hash.
    """
    repo = Repo(repo_path)
    # Fetch author and committer information from Git config
    author = str(repo.config_reader().get_value('user', 'name'))
    author_email = str(repo.config_reader().get_value('user', 'email'))
    committer = Actor(author, author_email)

    return repo.index.commit(
        message=message,
        committer=committer
    ).hexsha


def edit_message(orig: str) -> str:
    """
    Edit the commit message in the editor specified by the EDITOR environment variable.
    """
    editor = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(suffix=".tmp") as temp_file:
        temp_file.write(orig.encode())
        temp_file.flush()
        subprocess.call([editor, temp_file.name])

        temp_file.seek(0)
        # With open it and read it for result returning
        with open(temp_file.name, 'r', encoding='utf-8') as tmp_file:
            return tmp_file.read()


def get_commit_message() -> str:
    """
    Generate commit messages based on the configuration and prompt the user for confirmation.
    Return the selected commit message or an empty string if none is selected.
    """
    config_path = args['config']
    config = Config(config_path)

    for msg in generate_commit_message(config, CURRENT_PATH):
        print(msg)
        if config['interactive']:
            user_selection = get_user_input(
                'Is this commit message satisfactory? (Y/n/e) ', 'Y')
            if user_selection == 'Y':
                return msg
            if user_selection == 'n':
                continue
            if user_selection == 'e':
                return edit_message(msg)
        else:
            return msg

    return ''


def main() -> None:
    """
    Main function that generates and commits a message based on the configuration.
    """
    commit_message = get_commit_message()
    if commit_message:
        commit_hash = commit_full_text_message(CURRENT_PATH, commit_message)
        print(f'Commit message generated: {commit_hash}')
    else:
        print('No commit message generated. Exiting...')
        sys.exit(1)


if __name__ == '__main__':
    main()
