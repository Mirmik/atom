#!/usr/bin/env python3

from wheel.bdist_wheel import bdist_wheel as bdist_wheel_
from setuptools import setup, Extension, Command
from distutils.util import get_platform

import glob
import sys
import os

setup(
    name="atom",
    packages=["atom"],
    version="0.0.1",
    license="UNLICENSED",
    description="ATOM",
    author="mirmik",
    author_email="netricks@protonmail.com",
    url="https://github.com/mirmik/atom",
    classifiers=[],
    package_data={"atom": ["img/*"]},
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["atom=atom.__main__:main"]},
)
