#!/bin/bash

export IDF_VER=v5.0
export IDF_PATH=./esp-idf/$IDF_VER
export IDF_TARGETS=esp32,esp32s3

set -e
# cwd is the current directory of
cd "$(dirname "${BASH_SOURCE[0]}")"
# store the python path
python_path=$(which python) 
# if .espressif in python_path then display an error and exit
if [[ $python_path == *".espressif"* ]]; then
    echo "Error: You are using the espressif python environment. Please deactivate it and try again."
    exit 1
fi
if [ -d $IDF_PATH ]; then
    # warn the user that we are about to rm-rf ~/esp directory
    echo "Warning: This script will remove the $IDF_PATH directory and all its contents."
    read -p "Continue? [y/n]: " choice
    case $choice in
        y|Y) echo "Removing $IDF_PATH directory"
             ;;
        *) echo "Aborting"
           exit 1
           ;;
    esac
    rm -rf ~/esp
fi
rm -rf $IDF_PATH
mkdir -p $(dirname $IDF_PATH)
git clone -b $IDF_VER --recursive --depth 1 https://github.com/espressif/esp-idf.git $IDF_PATH 
cd $IDF_PATH
# Install WT32-SC01 (esp32) and WT32-SC01-Plus (esp32s3) toolchain
./install.sh $IDF_TARGETS
# Workaround a bug for the fmt library in managed components
