import os

from src.args import args
from src.config_parser import Config
from src.commit_msg_generator import generate_commit_message
from git import Repo, Actor

CURRENT_PATH = os.path.curdir


def get_user_input(prompt: str, default: str) -> str:
    user_input = input(f"{prompt} ({default})")
    if not user_input:
        return default
    return user_input


def commit_full_text_message(repo_path: str,
                             message: str) -> str:
    repo = Repo(repo_path)
    # Fetch author and committer information from Git config
    author = str(repo.config_reader().get_value('user', 'name'))
    author_email = str(repo.config_reader().get_value('user', 'email'))
    committer = Actor(author, author_email)

    return repo.index.commit(
        message=message,
        committer=committer
    ).hexsha


def get_commit_message() -> str:
    config_path = args['config']
    config = Config(config_path)

    for msg in generate_commit_message(config, CURRENT_PATH):
        print(msg)
        # Get user's input to decide whether to continue
        # If the user is satisfied, then break the loop
        # Otherwise, continue to generate commit message
        if config['interactive'] and get_user_input(
                'Is this commit message satisfactory? (Y/n)', 'Y') == 'Y':
            return msg
    return ''


def main() -> None:
    commit_message = get_commit_message()
    if commit_message:
        commit_hash = commit_full_text_message(
            CURRENT_PATH, commit_message)
        print(f'Commit message generated: {commit_hash}')
    else:
        print('No commit message generated. Exiting...')
        exit(1)


if __name__ == '__main__':
    main()
