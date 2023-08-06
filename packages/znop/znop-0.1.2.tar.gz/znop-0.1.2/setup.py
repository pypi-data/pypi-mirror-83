#!/usr/bin/env python

import sys

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    "wheel"
]

# Require python 3.7
if sys.version_info.major != 3 and sys.version_info.minor < 6:
    sys.exit("'Znop' requires Python >= 3.6!")

setup(
    name="znop",
    version="0.1.2", 
    author="Paaksing",
    author_email="paaksingtech@gmail.com",
    url="https://github.com/paaksing/Znop",
    description="Library that solves discrete math operations of the group Zn, provides both as calculator program or third party library.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["Math", "Discrete", "Group mod n", "Int mod n", "Zn"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
    ],
    license="MIT",
    packages=find_packages(exclude=("test")),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'znop=znop.__main__:run',
        ],
    },
)
