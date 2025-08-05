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

## Default usage

### BaseConverter Class

#### Constructor
```python
BaseConverter(default_precision=10)
```

`default_precision` (int): Default precision for fractional conversions (1-50)

#### Methods

**Decimal Conversions:**
- `decimal_to_binary(number, precision=None)`
- `decimal_to_octal(number, precision=None)`
- `decimal_to_hex(number, precision=None)`

**Binary Conversions:**
- `binary_to_decimal(number, precision=None)`
- `binary_to_octal(number, precision=None)`
- `binary_to_hex(number, precision=None)`

**Octal Conversions:**
- `octal_to_decimal(number, precision=None)`
- `octal_to_binary(number, precision=None)`
- `octal_to_hex(number, precision=None)`

**Hexadecimal Conversions:**
- `hex_to_decimal(number, precision=None)`
- `hex_to_binary(number, precision=None)`
- `hex_to_octal(number, precision=None)`

**Universal Converter:**
- `convert(number, from_base, to_base, precision=None)`

## Command Line Usage

```bash
# Convert decimal to binary
python -m base_converter 3.14159 --from-base 10 --to-base 2 --precision 8

# Convert hex to decimal
python -m base_converter "FF.8" --from-base 16 --to-base 10

# Convert binary to octal
python -m base_converter "1010.01" --from-base 2 --to-base 8
```

## Input Formats

The package accepts various input formats:

- **Decimal**: `3.14159`, `"3.14159"`
- **Binary**: `"1010.01"`, `"0b1010.01"`
- **Octal**: `"17.4"`, `"0o17.4"`
- **Hexadecimal**: `"FF.8"`, `"0xFF.8"`

## Error Handling

The package includes comprehensive error handling:

```python
from base_converter import ConversionError

try:
    result = converter.binary_to_decimal("102")  # Invalid binary
except ConversionError as e:
    print(f"Conversion error: {e}")
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

### Code Formatting

```bash
black base_converter/
flake8 base_converter/
```

If you like the project feel free to drop a star and follow :)
