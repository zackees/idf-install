# WORK IN PROGRESS

import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# Set environment variables
IDF_VER = "v5.0"
IDF_PATH = f"./esp-idf/{IDF_VER}"
IDF_TARGETS = "esp32,esp32s3,esp32c3"


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
    _ = parser.parse_args()
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

    # Create the directory
    os.makedirs(os.path.dirname(IDF_PATH), exist_ok=True)

    if os.path.exists(IDF_PATH):
        subprocess.run("git pull", cwd="esp-idf", shell=True, check=True)
    else:
        # Clone the repository
        subprocess.run(
            [
                "git",
                "clone",
                "-b",
                IDF_VER,
                "--recursive",
                "--depth",
                "1",
                "https://github.com/espressif/esp-idf.git",
                IDF_PATH,
            ],
            check=True,
        )

    os.chdir(IDF_PATH)

    print(f"About to run install script in the current directory: {os.path.abspath(os.getcwd())}")

    # Install WT32-SC01 (esp32) and WT32-SC01-Plus (esp32s3) toolchain
    if os.name == "nt":
        rtn = subprocess.run(f"cmd.exe /c install.bat {IDF_TARGETS}", shell=True, check=True)
    else:
        rtn = subprocess.run(["./install.sh", IDF_TARGETS], check=True)
    return rtn.returncode


if __name__ == "__main__":
    sys.exit(main())
