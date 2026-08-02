#!/usr/bin/env python3
"""
Setup script for Blackjack Game
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blackjack-game",
    version="1.0.0",
    author="DevAlchemy67",
    author_email="",
    description="A comprehensive Python blackjack game for beginners to advanced players",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DevAlchemy67/python_Starter_Code",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "blackjack=blackjack_game.main:main",
            "blackjack-trainer=blackjack_game.main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/DevAlchemy67/python_Starter_Code/issues",
        "Source": "https://github.com/DevAlchemy67/python_Starter_Code",
    },
)
