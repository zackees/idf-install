# idf-install

The missing installer for idf-installer for esp32 development. Run `idf-install` and an environment will be installed and files will be dropped to enter into the environment.

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

[![MacOS Install Test](https://github.com/zackees/idf-install/actions/workflows/macos_install.yml/badge.svg)](https://github.com/zackees/idf-install/actions/workflows/macos_install.yml)
[![Ubuntu Install Test](https://github.com/zackees/idf-install/actions/workflows/ubuntu_install.yml/badge.svg)](https://github.com/zackees/idf-install/actions/workflows/ubuntu_install.yml)
[![Windows Install Test](https://github.com/zackees/idf-install/actions/workflows/windows_install.yml/badge.svg)](https://github.com/zackees/idf-install/actions/workflows/windows_install.yml)

# Install idf-install toolset

Install the installer tool
```bash
pip install .
```

Then run the installer
```bash
idf-install
```

After that, run the `idf_activate` command to enter into the environment

Windows:
```bash
idf_activate.bat
```

Linux/MacOS
```bash
. ./idf_activate.sh
```

Then after this you are going to initialize the project

```bash
idf.py create-project myproject
```

Now cd into the directory and build it

```bash
cd myproject
idf.py build
```

Now you can flash the device

```bash
idf.py flash
# or idf.py -p (PORT) flash
```

And now you can monitor the device with

```bash
idf.py -p (PORT) monitor
```

# Develop

To develop software, run `. ./activate.sh`

## Windows

This environment requires you to use `git-bash`.

## Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.

# Versions
  * 1.0.5: Update readme.
  * 1.0.4: First release candidate of the project. See readme for details on using this.
