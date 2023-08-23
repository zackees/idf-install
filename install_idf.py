# WORK IN PROGRESS

import os
import sys
import subprocess
import shutil

# Set environment variables
IDF_VER = "v5.0"
IDF_PATH = f"./esp-idf/{IDF_VER}"
IDF_TARGETS = "esp32,esp32s3,esp32c3"

# Get the current directory of this script
cwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(cwd)

# Get the python path
python_path = shutil.which("python")

# Check if .espressif is in the python path
if ".espressif" in python_path:
    print("Error: You are using the espressif python environment. Please deactivate it and try again.")
    sys.exit(1)

# Check if IDF_PATH directory exists
if os.path.isdir(IDF_PATH):
    print(f"Warning: This script will remove the {IDF_PATH} directory and all its contents.")
    choice = input("Continue? [y/n]: ").lower()
    if choice == 'y':
        print(f"Removing {IDF_PATH} directory")
    else:
        print("Aborting")
        sys.exit(1)
    shutil.rmtree(IDF_PATH)

# Create the directory
os.makedirs(os.path.dirname(IDF_PATH), exist_ok=True)

# Clone the repository
subprocess.run(["git", "clone", "-b", IDF_VER, "--recursive", "--depth", "1", "https://github.com/espressif/esp-idf.git", IDF_PATH], check=True)

os.chdir(IDF_PATH)

print(f"About to run install script in the current directory: {os.path.abspath(os.getcwd())}")

# Install WT32-SC01 (esp32) and WT32-SC01-Plus (esp32s3) toolchain
if os.name == "nt":
    subprocess.run(f"cmd.exe /c install.bat {IDF_TARGETS}", shell=True, check=True)
else:
    subprocess.run(["./install.sh", IDF_TARGETS], check=True)
