"""
Floating Base Converter

A Python package for converting floating-point numbers between different bases
(decimal, binary, octal, hexadecimal).

Example:
    >>> from base_converter import BaseConverter
    >>> converter = BaseConverter()
    >>> result = converter.decimal_to_hex(3.14159, precision=6)
    >>> print(result)  # "3.243F6A"
"""

from .converter import BaseConverter
from .utils import validate_input, normalize_input, ConversionError

__version__ = "1.0.0"
__author__ = "Yeabwang"
__email__ = "wangxiayu@yeab.io"

__all__ = [
    "BaseConverter",
    "ConversionError",
    "validate_input",
    "normalize_input",
]
