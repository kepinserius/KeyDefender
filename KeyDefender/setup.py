#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="KeyDefender",
    version="1.0.0",
    author="KeyDefender Team",
    description="An anti-keylogger virtual keyboard application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/keydefender",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "keydefender=KeyDefender.src.main:main",
        ],
    },
) 