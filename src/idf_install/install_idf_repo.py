import os
import shutil
import subprocess
from warnings import warn

from send2trash import send2trash

from idf_install.settings import GIT_REPO


def install_idf_repo(idf_install_path: str, commit: str | None) -> None:
    # Use git to ensure repo is valid
    if os.path.exists(idf_install_path):
        shutil.rmtree(idf_install_path, ignore_errors=True)
        try:
            shutil.rmtree(idf_install_path)
        except OSError:
            warn(
                f"Could not fully remove {idf_install_path} using shutil.rmtree,"
                + " sending it to the trash instead."
            )
            send2trash(idf_install_path)

    # Full install: clone the repository
    print(f"Cloning the repository into directory {os.path.abspath(idf_install_path)}")
    print("grab a coffee... this will take a while.")
    git_clone_cmd = ["git", "clone", "--recursive", GIT_REPO, idf_install_path]
    subprocess.run(git_clone_cmd, check=True)
    # Checkout the specific commit
    if commit is not None:
        git_checkout_cmd = ["git", "checkout", commit]
        subprocess.run(git_checkout_cmd, check=True, cwd=idf_install_path)
