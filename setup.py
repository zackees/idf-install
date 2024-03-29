"""
Setup file.
"""

import os

from setuptools import setup

URL = "https://github.com/zackees/idf-install"
KEYWORDS = "esp32 idf install"
HERE = os.path.dirname(os.path.abspath(__file__))



if __name__ == "__main__":
    setup(
        maintainer="Zachary Vorhies",
        keywords=KEYWORDS,
        url=URL,
        package_data={"": ["assets/example.txt"]},
        include_package_data=True)

