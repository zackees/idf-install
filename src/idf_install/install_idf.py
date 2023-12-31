# WORK IN PROGRESS

import os
import shutil
import subprocess
import sys
import argparse

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
    args = parser.parse_args()
    def ask_user(msg: str) -> bool:
        if args.non_interactive:
            return True
        else:
            choice = input(msg).lower()
            if choice == "y":
                return True
            else:
                return False
    # Get the python path
    python_path = shutil.which("python")
    assert python_path is not None, "Python not found in PATH"

    # Check if .espressif is in the python path
    if ".espressif" in python_path:
        print(
            "Error: You are using the espressif python environment. Please deactivate it and try again."
        )
        sys.exit(1)

    # Check if IDF_PATH directory exists
    if os.path.isdir(IDF_PATH):
        print(
            f"Warning: This script will remove the {IDF_PATH} directory and all its contents."
        )
        do_continue = ask_user("Continue? [y/n]: ")
        if do_continue:
            print(f"Removing {IDF_PATH} directory")
        else:
            print("Aborting")
            sys.exit(1)
        shutil.rmtree(IDF_PATH)

    # Create the directory
    os.makedirs(os.path.dirname(IDF_PATH), exist_ok=True)

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

    print(
        f"About to run install script in the current directory: {os.path.abspath(os.getcwd())}"
    )

    # Install WT32-SC01 (esp32) and WT32-SC01-Plus (esp32s3) toolchain
    if os.name == "nt":
        subprocess.run(f"cmd.exe /c install.bat {IDF_TARGETS}", shell=True, check=True)
    else:
        subprocess.run(["./install.sh", IDF_TARGETS], check=True)


if __name__ == "__main__":
    sys.exit(main())