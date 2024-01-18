import os
import subprocess
from warnings import warn


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
        # Generate an export.bat file that simply calls into the export_bat file in the toolchain.
    else:
        cp = subprocess.run(
            ["./install.sh", idf_targets], check=True, cwd=idf_install_path
        )
        files = find_files("export.sh", idf_install_path, break_on_first_match=True)
        if len(files) == 0:
            warn(f"export.sh not found in {idf_install_path}")
            return cp

    files = find_files("export.bat", idf_install_path, break_on_first_match=True)
    if len(files) == 0:
        warn(f"export.bat not found in {idf_install_path}")
        return cp
    # Now write out the entrypoint script to activate the toolchain.
    export_bat = files[0]
    # make it relative
    export_bat = os.path.relpath(export_bat, os.getcwd())
    with open("idf_activate.bat", encoding="utf-8", mode="w") as f:
        f.write(f'@call "{export_bat}"\n')
    print("\nNow run idf_activate.bat whenever you want to use the idf.py toolchain.")
    export_sh = files[0]
    # make it relative
    export_sh = os.path.relpath(export_sh, os.getcwd())
    # Generate an export.sh file that simply calls into the export_sh file in the toolchain.
    with open("idf_activate.sh", encoding="utf-8", mode="w") as f:
        f.write(f'source "{export_sh}"\n')
    if os.name == "nt":
        print(
            "\nNow run source idf_activate.bat whenever you want to use the idf.py"
            + " toolchain or use the idf.py toolchain in WSL/git-bash."
        )
    else:
        print(
            "\nNow run source idf_activate.sh whenever you want to use the idf.py toolchain."
        )

    return cp
