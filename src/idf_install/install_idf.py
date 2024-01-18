import argparse
import os
import shutil
import sys
from warnings import warn

from idf_install.install_idf_repo import install_idf_repo
from idf_install.platform_install import run_platform_install
from idf_install.util import touch_file

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INSTALL_DIR = os.path.join(os.getcwd(), "esp-idf")

# Set environment variables
IDF_VER = "v5.2"  # Only used to version downloaded files.
DEFAULT_IDF_TARGETS = "esp32,esp32s3,esp32c3"

sys.setrecursionlimit(200)  # Increase the limit, 2000 is just an example


COMMIT_MAP = {
    # Maps IDF_VER to the commit hash
    "v5.2": "b3f7e2c8a4d354df8ef8558ea7caddc07283a57b",
    "latest": None,
}


def check_git_ignore() -> None:
    # Check if the .gitignore file is present
    is_git_repo = os.path.exists(os.path.join(HERE, ".git"))
    if not is_git_repo:
        return
    gitignore_path = os.path.join(HERE, ".gitignore")
    touch_file(gitignore_path)
    with open(gitignore_path, encoding="utf-8", mode="r") as f:
        gitignore = f.read()
    if "esp-idf" not in gitignore:
        print(f"adding esp-idf to {gitignore_path}")
        with open(gitignore_path, encoding="utf-8", mode="a") as f:
            f.write("\nesp-idf\n\nidf_activate.bat\nidf_activate.sh\n")


def check_environment() -> tuple[bool, str]:
    python_path = shutil.which("python") or shutil.which("python3")
    if python_path is None:
        return False, "Python not found in PATH"

    # Check if .espressif is in the python path
    if ".espressif" in python_path:
        print(
            "Error: You are using the espressif python environment."
            "Please deactivate it and try again."
        )
        # return 1
        return False, (
            "Error: You are using the espressif python environment."
            "Please deactivate it and try again."
        )
    return True, ""


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install ESP-IDF toolchain",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--esp32-targets",
        help=f"Install the ESP32 toolchain: default is {DEFAULT_IDF_TARGETS}",
        type=str,
        default=DEFAULT_IDF_TARGETS,
    )
    # --non-interactive
    parser.add_argument(
        "--non-interactive",
        help="Do not ask for confirmation before removing the directory",
        action="store_true",
    )
    parser.add_argument(
        "--latest",
        help="Install the latest version of the IDF",
        action="store_true",
    )
    parser.add_argument(
        "--install-dir",
        help=f"Directory to install the IDF to, default is {DEFAULT_INSTALL_DIR}",
        type=str,
        default=DEFAULT_INSTALL_DIR,
    )
    args = parser.parse_args()
    return args


def main() -> int:
    args = parse_arguments()
    if args.non_interactive:
        warn("non-interactive mode is not implemented yet.")
    ok, err_msg = check_environment()
    if not ok:
        print(err_msg)
        return 1
    if args.latest:
        commit = None
        idf_install_path = os.path.join(args.install_dir, "latest")
    else:
        commit = COMMIT_MAP[IDF_VER]
        idf_install_path = os.path.join(args.install_dir, IDF_VER)
    print(f"install idf at: {idf_install_path}")
    install_idf_repo(idf_install_path, commit)
    print(
        f"About to run install script in the current directory: {os.path.abspath(idf_install_path)}"
    )

    targets = args.esp32_targets
    completed_process = run_platform_install(idf_install_path, targets)
    if completed_process.returncode != 0:
        print("Error: Platform installation failed.")
    return completed_process.returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Cancelled by user.")
        sys.exit(1)
