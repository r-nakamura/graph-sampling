#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="graph-sampling",
    version="1.0",
    author="Ryo Nakamura",
    author_email="nakamura@insl.jp",
    description="A set of tools for graph sampling",
    packages=setuptools.find_packages(),
    install_requires=['graph_tools', 'randwalk', 'perlcompat'],
    scripts=['bin/graphsampl'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
