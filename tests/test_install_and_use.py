"""
Unit test file.
"""

import os
import tempfile
import unittest

from idf_install.util import safe_rmtree

TEST_GITHUB = "https://github.com/zackees/xiao-inmp441-test"
IS_GITHUB = os.getenv("GITHUB_ACTIONS") is not None


class InstallAndUse(unittest.TestCase):
    """Main tester class."""

    def test_install(self) -> None:
        """Test command line interface (CLI)."""
        original_cwd = os.getcwd()
        tmpdir = tempfile.mkdtemp()
        os.chdir(tmpdir)
        rtn = os.system(f"git clone {TEST_GITHUB} app")
        self.assertEqual(0, rtn)
        prev_cwd = os.getcwd()
        os.chdir("app")
        rtn = os.system("idf-install --non-interactive")
        self.assertEqual(0, rtn)
        is_windows = os.name == "nt"
        if is_windows:
            rtn = os.system("idf_activate.bat && idf.py --help")
        else:
            rtn = os.system("source idf_activate.sh && idf.py --help")
        self.assertEqual(0, rtn)
        os.chdir(prev_cwd)
        safe_rmtree("app")
        os.chdir(original_cwd)
        safe_rmtree(tmpdir)


if __name__ == "__main__":
    unittest.main()
