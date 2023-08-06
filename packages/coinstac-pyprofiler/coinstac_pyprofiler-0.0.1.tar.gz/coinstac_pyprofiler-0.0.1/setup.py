"""
Created on Mon Oct 26 16:23:24 2020

@author: Sunitha Basodi
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setuptools.setup(
    name="coinstac_pyprofiler",  # Replace with your own username
    version="0.0.1",
    author="Sunitha Basodi",
    author_email="sunitha.basodi@gmail.com",
    description="A wrapper for some existing python profilers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',

    install_requires=required_packages
)
