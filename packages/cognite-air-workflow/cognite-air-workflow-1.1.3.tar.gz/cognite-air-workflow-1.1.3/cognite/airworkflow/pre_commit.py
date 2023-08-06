from pathlib import Path

from git import Repo

import cognite.airworkflow.constants as const
from cognite.airworkflow.master_config import get_master_config


def add_path_to_git(path: Path) -> None:
    repo = Repo(const.ROOT_DIR)
    if path.is_file():
        add_file_to_git(repo, path)
    else:
        for f in path.iterdir():
            if f.is_file():
                repo.git.execute(["git", "add", str(f)])


def add_file_to_git(repo: Repo, path: Path) -> None:
    repo.git.execute(["git", "add", str(path)])


def commit_to_git() -> None:
    repo = Repo(const.ROOT_DIR)
    repo.git.execute(["git", "commit", "--amend", "-C", "HEAD", "--no-verify"])


if __name__ == "__main__":
    """
    Load, validate and merge the individual function configs.
    """
    get_master_config()
    add_path_to_git(const.WORK_FLOW_PATH)
