#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import setuptools

from atlas_client import __version__ as version

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
with open(requirements_path) as requirements_file:
    requirements = requirements_file.readlines()

setuptools.setup(
    name="atlaspyapi",  # Replace with your own username
    version=version,
    author="Pengfei Liu",
    author_email="pengfei.liu@insee.fr",
    description="This atlas python api can generate atlas entities and import them into a"
                "Atlas instances.",
    license='Apache License 2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.lab.sspcloud.fr/pengfei/atlaspyapi",
    # we need to indicate excitement which package will be published, otherwise import will raise module name not found
    packages=setuptools.find_packages(include=['atlas_client', 'atlas_client.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    include_package_data=True,
    package_data={'': ['entity_source_generation/template/*.j2', 'config/*.ini']},
    python_requires='>=3.7',

)
