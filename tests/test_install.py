"""
Unit test file.
"""

import unittest
import sys

from idf_install.install_idf import main

class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_install(self) -> None:
        """Test command line interface (CLI)."""
        sys.argv.append("--non-interactive")
        rtn = main()
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
