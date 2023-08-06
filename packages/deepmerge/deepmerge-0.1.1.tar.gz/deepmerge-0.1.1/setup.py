#!/usr/bin/env python
import os
import sys

is_release = False
if "--release" in sys.argv:
    sys.argv.remove("--release")
    is_release = True
from setuptools import setup, find_packages

base = os.path.dirname(os.path.abspath(__file__))

README_PATH = os.path.join(base, "README.rst")

install_requires = []

tests_require = []

setup(
    name="deepmerge",
    setup_requires=["vcver"],
    vcver={"is_release": is_release, "path": base},
    description="a toolset to deeply merge python dictionaries.",
    long_description=open(README_PATH).read(),
    author="Yusuke Tsutsumi",
    author_email="yusuke@tsutsumi.io",
    url="http://deepmerge.readthedocs.io/en/latest/",
    packages=find_packages(exclude=["*.tests*"]),
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    tests_require=tests_require,
)