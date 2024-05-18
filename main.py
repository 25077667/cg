"""The main script for the commit message generator"""

import os
import sys
import logging
from src.args import args
from src.config_parser import Config
from src.git_utils import get_repo_path, commit_full_text_message
from src.user_interaction import get_user_input, edit_message
from src.commit_msg_generator import generate_commit_message


def main():
    """The main function of the script"""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    config_path = args["config"]
    config = Config(config_path)
    repo_path = get_repo_path(os.getcwd())

    # Generate commit messages
    commit_messages = generate_commit_message(config, repo_path)

    # Present the generated commit message to the user and get confirmation
    for message in commit_messages:
        print(f"Suggested commit message:\n\n{message}\n")
        if config["interactive"]:
            user_selection = get_user_input(
                "Is this commit message satisfactory? (Y/n/e) ", "Y"
            ).lower()
            if user_selection == "y":
                final_message = message
            elif user_selection == "n":
                continue
            elif user_selection == "e":
                final_message = edit_message(message)
            else:
                print("Invalid selection. Please choose Y, n, or e.")
                continue
        else:
            final_message = message

        commit_hash = commit_full_text_message(repo_path, final_message)
        print(f"Commit successful with hash: {commit_hash}")
        break
    else:
        print("No commit message generated. Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()
