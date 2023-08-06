#! /usr/bin/env python3
# coding=utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrcssscom-cangyin", # Replace with your own username
    version="0.0.1",
    author="cangyin",
    author_email="excangyin@gmail.com",
    description="simple communication with rcssserver3d server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(where='.', exclude=[], include=['rcssscom']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
