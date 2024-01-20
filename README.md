# idf-install

The missing installer for idf-installer for esp32 development. Run `idf-install` and an environment will be installed and files will be dropped to enter into the environment.

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

[![Install Test](https://github.com/zackees/idf-install/actions/workflows/install.yml/badge.svg)](https://github.com/zackees/idf-install/actions/workflows/install.yml)

# Install idf-install toolset

Install the installer tool
```
pip install .
```

Then run the installer
```
idf-install
```

After that, run the `idf_activate` command to enter into the environment

Windows:
```
idf_activate.bat
```

Linux/MacOS
```
. ./idf_activate.sh
```

Then after this you are going to initialize the project

```
idf.py create-project myproject
```

Now cd into the directory and build it

```
cd myproject
idf.py build
```

Now you can flash the device

```
idf.py flash
# or idf.py -p (PORT) flash
```

And now you can monitor the device with

```
idf.py -p (PORT) monitor
```

# Develop

To develop software, run `. ./activate.sh`

## Windows

This environment requires you to use `git-bash`.

## Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.

# Versions

  * 1.0.4: First release candidate of the project. See readme for details on using this.
