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
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=IS_GITHUB) as tmpdir:
            os.chdir(tmpdir)
            rtn = os.system(f"git clone {TEST_GITHUB} app")
            self.assertEqual(0, rtn)
            prev_cwd = os.getcwd()
            os.chdir("app")
            rtn = os.system("idf-install --non-interactive")
            self.assertEqual(0, rtn)
            os.chdir(prev_cwd)
            safe_rmtree("app")


if __name__ == "__main__":
    unittest.main()
