"""
Copyright (C) Kehtra Pty Ltd - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyram-sa',
    version='0.0.1',
    author='Jordy Chetty',
    author_email='jxrrdy@gmail.com',
    description='A Python client for RAM web services',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kehtra/PyRAM",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)