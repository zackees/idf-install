import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Set environment variables
IDF_VER = "v5.2"  # Only used to version downloaded files.
DEFAULT_IDF_TARGETS = "esp32,esp32s3,esp32c3"
GIT_REPO = "https://github.com/espressif/esp-idf.git"

COMMIT_MAP = {
    # Maps IDF_VER to the commit hash
    "v5.2": "b3f7e2c8a4d354df8ef8558ea7caddc07283a57b",
    "latest": None,
}


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
    else:
        cp = subprocess.run(
            ["./install.sh", idf_targets], check=True, cwd=idf_install_path
        )
    return cp


def git_ensure_installed(idf_install_path: str, commit: str | None) -> None:
    # Use git to ensure repo is valid
    if os.path.exists(idf_install_path):
        shutil.rmtree(idf_install_path)

    # Full install: clone the repository
    print(f"Cloning the repository into directory {os.path.abspath(idf_install_path)}")
    print("grab a coffee... this wil take a while.")
    git_clone_cmd = ["git", "clone", "--recursive", GIT_REPO, idf_install_path]
    subprocess.run(git_clone_cmd, check=True)
    # Checkout the specific commit
    if commit is not None:
        git_checkout_cmd = ["git", "checkout", commit]
        subprocess.run(git_checkout_cmd, check=True, cwd=idf_install_path)


def check_git_ignore() -> None:
    # Check if the .gitignore file is present
    gitignore_path = os.path.join(HERE, ".gitignore")
    if not os.path.exists(gitignore_path):
        print(
            f"Warning: {gitignore_path} not found. "
            "This may cause issues with the installation."
        )
        return
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


def main() -> int:
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
    # do something with args later.
    args = parser.parse_args()
    if args.non_interactive:
        raise NotImplementedError("Non-interactive mode is not supported yet.")
    # Get the python path
    ok, err_msg = check_environment()
    if not ok:
        print(err_msg)
        return 1
    if args.latest:
        commit = None
        idf_install_path = "./esp-idf/latest"
    else:
        commit = COMMIT_MAP[IDF_VER]
        idf_install_path = f"./esp-idf/{IDF_VER}"
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
    sys.exit(main())
