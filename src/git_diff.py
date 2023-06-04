# Generate git diff for added files and the head commit
from git import Repo


def git_diff(repo_path: str) -> str:
    repo = Repo(repo_path)
    return repo.git.diff('HEAD', name_only=True)
