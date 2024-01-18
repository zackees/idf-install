import os
import shutil
from warnings import warn

from send2trash import send2trash


def touch_file(filepath: str) -> None:
    with open(filepath, mode="a"):  # pylint: disable=unspecified-encoding
        pass


def safe_rmtree(path: str) -> None:
    """Delete a directory, but send it to the trash if it fails."""

    is_windows = os.name == "nt"
    if is_windows:
        os.system(f'rmdir /S /Q "{path}"')
    else:
        os.system(f'rm -rf "{path}"')

    if not os.path.exists(path):
        return

    shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):
        return
    if os.path.exists(path):
        warn(
            f"Could not fully remove {path} using shutil.rmtree,"
            + " sending it to the trash instead."
        )
        send2trash(path)
    if os.path.exists(path):
        warn(f"Could not remove {path}")
