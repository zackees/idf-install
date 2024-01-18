import os
import shutil
import stat
from warnings import warn

from send2trash import send2trash


def touch_file(filepath: str) -> None:
    with open(filepath, mode="a"):  # pylint: disable=unspecified-encoding
        pass


def onerror(func, path, exc_info):  # pylint: disable=unused-argument
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    if not os.path.exists(path):
        return

    # Is the error an access error?
    if not os.access(path, os.W_OK):
        try:
            os.chmod(path, stat.S_IWUSR)
            func(path)
        except PermissionError:
            return
    else:
        return


def safe_rmtree(path: str) -> None:
    """Delete a directory, but send it to the trash if it fails."""
    shutil.rmtree(path, ignore_errors=True)
    if not os.path.exists(path):
        return

    shutil.rmtree(path, onerror=onerror)
    if not os.path.exists(path):
        return
    if os.path.exists(path):
        is_windows = os.name == "nt"
        if is_windows:
            os.system(f'rmdir /S /Q "{path}"')
    if os.path.exists(path):
        warn(
            f"Could not fully remove {path} using shutil.rmtree,"
            + " sending it to the trash instead."
        )
        send2trash(path)
    if os.path.exists(path):
        warn(f"Could not remove {path}")
