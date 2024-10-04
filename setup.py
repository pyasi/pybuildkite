#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybuildkite",
    version="1.2.4",
    url="https://github.com/pyasi/pybuildkite",
    download_url="https://github.com/pyasi/pybuildkite/archive/master.zip",
    author="Peter Yasi",
    packages=["pybuildkite"],
    description="Python wrapper for the Buildkite API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["Buildkite", "Continuous Integration", "API", "CI", "wrapper", "python"],
    install_requires=["requests"],
)
