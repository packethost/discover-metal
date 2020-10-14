#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="equinix-discover-metal",
    version="1.0",
    description="Tool used to discover important details about a piece of hardware.",
    author="Equinix Metal",
    author_email="support@equinixmetal.com",
    url="https://github.com/packethost/discover-metal/",
    packages=find_packages(),
    install_requires=["click", "lxml", "requests"],
    entry_points="""
        [console_scripts]
        discover-metal=discovermetal.cli:cli
    """,
)
