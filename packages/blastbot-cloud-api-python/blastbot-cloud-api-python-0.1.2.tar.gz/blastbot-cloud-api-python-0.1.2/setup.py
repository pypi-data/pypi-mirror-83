#!/usr/bin/env python

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='blastbot-cloud-api-python',
    version='0.1.2',
    description='Library for interfacing with Blastbot Cloud',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Rodrigo Mendez',
    author_email='rmendez@makerlab.mx',
    license="Apache License Version 2.0",
    url='https://github.com/Rodmg/blastbot-cloud-api-python',
    packages=find_packages(exclude=['tests*']),
    install_requires=["aiohttp"],
)
