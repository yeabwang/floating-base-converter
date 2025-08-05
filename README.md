# Floating Base Converter

A Python package for converting floating-point numbers between different number bases (decimal, binary, octal, hexadecimal).

## Features

- Convert between decimal (base 10), binary (base 2), octal (base 8), and hexadecimal (base 16)
- Support for floating-point numbers with customizable precision
- Handle both string and numeric inputs
- Command-line interface included
- Comprehensive error handling
- Full test coverage

## Installation

```bash
pip install floating-base-converter
```

## Quick Start

```python
from base_converter import BaseConverter

# Create converter instance
converter = BaseConverter(default_precision=10)

# Convert decimal to other bases
print(converter.decimal_to_binary(3.14159))    # "11.001001000011111101101"
print(converter.decimal_to_hex(255.5))         # "FF.8"
print(converter.decimal_to_octal(8.75))        # "10.6"

# Convert from other bases to decimal
print(converter.binary_to_decimal("1010.01"))  # "10.25"
print(converter.hex_to_decimal("A.8"))          # "10.5"
print(converter.octal_to_decimal("17.4"))       # "15.5"

# Universal converter
print(converter.convert("FF", from_base=16, to_base=2))  # "11111111"
```

## CLI usage
```bash
# Convert decimal to binary
base-converter 3.14159 --from-base 10 --to-base 2 --precision 8

# Convert hex to decimal
base-converter "FF.8" --from-base 16 --to-base 10

# Convert binary to octal
base-converter "1010.01" --from-base 2 --to-base 8
```

## Development
If you think of something not implemneted and if you want to contribute checkout the CONTRIBUTING.md for development setup and guidelines.

## License
MIT License - see LICENSE file for details.

## Setup
`requirements.txt`
## No runtime dependencies required
 `requirements-dev.txt`

 If you find a small value in this please follow and drop a star :)