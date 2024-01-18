import shutil
from warnings import warn

from send2trash import send2trash


def touch_file(filepath: str) -> None:
    with open(filepath, mode="a"):  # pylint: disable=unspecified-encoding
        pass


def safe_rmtree(path: str) -> None:
    """Delete a directory, but send it to the trash if it fails."""
    shutil.rmtree(path, ignore_errors=True)
    try:
        shutil.rmtree(path)
    except OSError:
        warn(
            f"Could not fully remove {path} using shutil.rmtree,"
            + " sending it to the trash instead."
        )
        send2trash(path)
