"""
General utility functions for user interaction.
"""

import tempfile
import subprocess
from .git_utils import get_git_editor


def get_user_input(prompt: str, default: str) -> str:
    """
    Prompt the user for input and return the input value or the default value.
    """
    user_input = input(f"{prompt} [{default}]: ")
    return user_input.strip() or default


def edit_message(message: str) -> str:
    """
    Open the provided message in a text editor and return the edited message.
    """
    editor = get_git_editor()
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(message.encode())
        tf.flush()
        subprocess.call([editor, tf.name])
        tf.seek(0)
        edited_message = tf.read().decode()
    return edited_message
