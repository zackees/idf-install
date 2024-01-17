# idf-install

The missing installer for idf-installer for esp32 development. Run `idf-install` and an environment will be installed and files will be dropped to enter into the environment.

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

# Install idf-install toolset

Install the installer tool
```
pip install .
```

Then run the installer
```
idf-install
```

After that, run the export command to enter into the environment


Windows:
```
esp-idf\v5.2\export.bat
```

# Develop

To develop software, run `. ./activate.sh`

## Windows

This environment requires you to use `git-bash`.

## Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.
