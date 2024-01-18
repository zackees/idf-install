import argparse
import os
import shutil
import subprocess
import sys
from warnings import warn

from send2trash import send2trash

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INSTALL_DIR = os.path.join(os.getcwd(), "esp-idf")

# Set environment variables
IDF_VER = "v5.2"  # Only used to version downloaded files.
DEFAULT_IDF_TARGETS = "esp32,esp32s3,esp32c3"
GIT_REPO = "https://github.com/espressif/esp-idf.git"

COMMIT_MAP = {
    # Maps IDF_VER to the commit hash
    "v5.2": "b3f7e2c8a4d354df8ef8558ea7caddc07283a57b",
    "latest": None,
}


def find_files(
    filename: str, search_path: str, break_on_first_match: bool
) -> list[str]:
    result: list[str] = []
    # Wlaking top-down from the root
    for root, _, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
            if break_on_first_match:
                break
    return result


def run_platform_install(
    idf_install_path: str, idf_targets: str
) -> subprocess.CompletedProcess:
    # Run the install script for the platform
    # Install WT32-SC01 (esp32) and WT32-SC01-Plus (esp32s3) toolchain
    if os.name == "nt":
        cp = subprocess.run(
            f"cmd.exe /c install.bat {idf_targets}",
            shell=True,
            check=True,
            cwd=idf_install_path,
        )
        files = find_files("export.bat", idf_install_path, break_on_first_match=True)
        if len(files) == 0:
            warn(f"export.bat not found in {idf_install_path}")
            return cp
        export_bat = files[0]
        # make it relative
        export_bat = os.path.relpath(export_bat, os.getcwd())
        # Generate an export.bat file that simply calls into the export_bat file in the toolchain.
        with open("enter.bat", encoding="utf-8", mode="w") as f:
            f.write(f'@call "{export_bat}"\n')
        print("\nNow run enter.bat whenever you want to use the idf.py toolchain.")
    else:
        cp = subprocess.run(
            ["./install.sh", idf_targets], check=True, cwd=idf_install_path
        )
    return cp


def touch_file(filepath: str) -> None:
    with open(filepath, mode="a"):  # pylint: disable=unspecified-encoding
        pass


def git_ensure_installed(idf_install_path: str, commit: str | None) -> None:
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
            f.write("\nesp-idf\n")


def check_environment() -> tuple[bool, str]:
    python_path = shutil.which("python")
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
    return True, python_path


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
    git_ensure_installed(idf_install_path, commit)
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
