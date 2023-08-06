#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Setuptools script for ci_api_wrapper."""

import setuptools

with open("README.md", "r", encoding="iso-8859-1") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ci-api-wrapper",
    version="0.1",
    author="Joshua Brooke",
    author_email="joshua.brooke@nationalgrideso.com",
    description="A python wrapper for the UK Carbon Intensity API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Joshua-Brooke/Carbon-Intensity-API-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
