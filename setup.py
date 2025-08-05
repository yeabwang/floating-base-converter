from setuptools import setup, find_packages
import os

# Read README with error handling
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A Python package for converting floating-point numbers between different bases"

setup(
    name="floating-base-converter",
    version="0.1.0",
    author="Yeabwang",
    author_email="wangxiayu@yeab.io",
    description="A Python package for converting floating-point numbers between different bases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yeabwang/floating-base-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "twine>=4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "base-converter=base_converter.cli:main",
        ],
    },
    keywords="base conversion, floating point, binary, octal, hexadecimal, decimal",
)