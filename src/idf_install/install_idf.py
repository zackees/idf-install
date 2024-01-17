import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# Set environment variables
IDF_VER = "v5.2"  # Only used to version downloaded files.
IDF_INSTALL_PATH = f"./esp-idf/{IDF_VER}"
IDF_TARGETS = ["esp32", "esp32s3", "esp32c3"]

GIT_REPO = "https://github.com/espressif/esp-idf.git"

COMMIT_MAP = {
    # Maps IDF_VER to the commit hash
    "v5.2": "da6325dd7e8e152094b19fe63190907f38ef1ff0",
}


def get_commit() -> str:
    return COMMIT_MAP[IDF_VER]


def run_platform_install() -> subprocess.CompletedProcess:
    # Run the install script for the platform
    idf_targets_str = ",".join(IDF_TARGETS)
    # Install WT32-SC01 (esp32) and WT32-SC01-Plus (esp32s3) toolchain
    if os.name == "nt":
        cp = subprocess.run(
            f"cmd.exe /c install.bat {idf_targets_str}",
            shell=True,
            check=True,
            cwd=IDF_INSTALL_PATH,
        )
    else:
        cp = subprocess.run(["./install.sh", idf_targets_str], check=True, cwd=IDF_INSTALL_PATH)
    return cp


def git_ensure_installed(commit: str) -> None:
    # Use git to ensure repo is valid
    if os.path.exists(IDF_INSTALL_PATH):
        subprocess.run(["git", "clean", "-fdx"], cwd=IDF_INSTALL_PATH, check=True)
        subprocess.run(["git", "reset", "--hard"], cwd=IDF_INSTALL_PATH, check=True)
        subprocess.run(["git", "pull"], cwd=IDF_INSTALL_PATH, check=True)
    else:
        # Clone the repository
        with tempfile.TemporaryDirectory() as tmpdir:
            print("Cloning the repository into a temporary directory: ", tmpdir)
            subprocess.run(
                ["git", "clone", "--recursive", GIT_REPO, IDF_INSTALL_PATH],
                check=True,
                cwd=tmpdir,
            )
            # now copy the files to the current directory
            shutil.move(tmpdir, IDF_INSTALL_PATH)
    # Checkout the specific commit
    subprocess.run(["git", "checkout", commit], check=True, cwd=IDF_INSTALL_PATH)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install ESP-IDF toolchain",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # --non-interactive
    parser.add_argument(
        "--non-interactive",
        help="Do not ask for confirmation before removing the directory",
        action="store_true",
    )
    # do something with args later.
    args = parser.parse_args()
    if args.non_interactive:
        raise NotImplementedError("Non-interactive mode is not supported yet.")
    # Get the python path
    python_path = shutil.which("python")
    assert python_path is not None, "Python not found in PATH"

    # Check if .espressif is in the python path
    if ".espressif" in python_path:
        print(
            "Error: You are using the espressif python environment."
            "Please deactivate it and try again."
        )
        sys.exit(1)
    commit = get_commit()
    git_ensure_installed(commit)
    print(
        f"About to run install script in the current directory: {os.path.abspath(IDF_INSTALL_PATH)}"
    )
    completed_process = run_platform_install()
    if completed_process.returncode != 0:
        print("Error: Platform installation failed.")
    return completed_process.returncode


if __name__ == "__main__":
    sys.exit(main())
