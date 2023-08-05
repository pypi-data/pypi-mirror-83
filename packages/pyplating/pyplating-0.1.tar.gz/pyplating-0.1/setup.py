#!/usr/bin/env python3

import setuptools

with open("README.md") as f:
    long_desc = f.read()

setuptools.setup(
    name="pyplating",
    version="0.1",
    author="Max Black",
    author_email="maxoblack@yahoo.com",
    description="Python templating library with support for nesting",
    long_description_content_type="text/markdown",
    url="https://github.com/WiredSound/pyplating",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
