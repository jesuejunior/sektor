#!/usr/bin/env python
# enconding: utf-8
import sys
import os
from setuptools import setup, find_packages

from sektor import __version__

BASE_PATH = os.path.dirname(__file__)
setup(
    name="sektor",
    version=__version__,
    description="It is a robot to oil your motorcycle chain every 300KM ",
    long_description=open(os.path.join(BASE_PATH, "README.md")).read(),
    author="Jesue Junior",
    author_email="jesuesousa@gmail.com",
    url="https://github.com/jesuejunior/sektor",
    packages=find_packages(),
    install_requires=[],
    test_suite="tests",
    tests_require=["tox>=3.3.0", "pytest==3.8.0", "pytest-cov==2.6.0"]
    + (["mock==2.0.0"] if sys.version_info.major == 2 else []),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
