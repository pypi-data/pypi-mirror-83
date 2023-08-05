#!/usr/bin/env python
"""The setup script."""
import os
import re
import sys

from setuptools import find_packages, setup


def get_version():
    """Get current version from code."""
    regex = r"__version__\s=\s\"(?P<version>[\d\.]+?)\""
    path = ("bsblan", "__version__.py")
    return re.search(regex, read(*path)).group("version")


def read(*parts):
    """Read file."""
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)
    sys.stdout.write(filename)
    with open(filename, encoding="utf-8", mode="rt") as fp:
        return fp.read()


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Willem-Jan van Rootselaaar",
    author_email="liudgervr@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Asynchronous Python client for BSBLan.",
    include_package_data=True,
    install_requires=["aiohttp>=3.0.0", "attrs>=19.0.0", "cattrs", "yarl"],
    keywords=["bsblan", "api", "async", "client"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    name="bsblan",
    packages=find_packages(include=["bsblan"]),
    test_suite="tests",
    url="https://github.com/liudger/python-bsblan",
    version=get_version(),
    zip_safe=False,
)
