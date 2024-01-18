"""
Unit test file.
"""

import os
import tempfile
import unittest

from idf_install.util import safe_rmtree

TEST_GITHUB = "https://github.com/zackees/xiao-inmp441-test"


class InstallAndUse(unittest.TestCase):
    """Main tester class."""

    def test_install(self) -> None:
        """Test command line interface (CLI)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            rtn = os.system(f"git clone {TEST_GITHUB} app")
            self.assertEqual(0, rtn)
            os.chdir("app")
            rtn = os.system("idf-install --non-interactive")
            self.assertEqual(0, rtn)
            safe_rmtree("app")


if __name__ == "__main__":
    unittest.main()
