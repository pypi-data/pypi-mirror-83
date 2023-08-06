#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools

# Show README.md as PyPI "Project description".
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# utf-8 encoding is for tree symbols: └─, ├─, etc.

setuptools.setup(
    name="pygstuff", # do not use dashes or underscores in names!
    version="0.0.3", # must increment this to re-upload
    author="Mike Gazes",
    author_email="sustainablelab@gmail.com",
    description="PYGame Stuff for writing pygame applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sustainablelab/pygstuff",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    python_requires='>=3.7',
    install_requires=[
        "pygame",
        ],
    license='MIT', # field in *.egg-info/PKG-INFO
    platforms=['Windows', 'Mac', 'Linux'], # legacy field in *.egg-info/PKG-INFO
)
