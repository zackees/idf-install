import os
import subprocess

from idf_install.settings import GIT_REPO
from idf_install.util import safe_rmtree


def install_idf_repo(idf_install_path: str, commit: str | None) -> None:
    # Use git to ensure repo is valid
    safe_rmtree(idf_install_path)

    # Full install: clone the repository
    print(f"Cloning the repository into directory {os.path.abspath(idf_install_path)}")
    print("grab a coffee... this will take a while.")
    git_clone_cmd = ["git", "clone", "--recursive", GIT_REPO, idf_install_path]
    subprocess.run(git_clone_cmd, check=True)
    # Checkout the specific commit
    if commit is not None:
        git_checkout_cmd = ["git", "checkout", commit]
        subprocess.run(git_checkout_cmd, check=True, cwd=idf_install_path)
