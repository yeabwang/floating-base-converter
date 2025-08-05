# floating-base-converter

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](htmlcov/)

High-performance floating-point number base conversion library supporting decimal, binary, octal, and hexadecimal number systems.

## Features

- **Zero dependencies** - Pure Python implementation
- **High precision** - Configurable fractional precision (1-50 digits)
- **Multiple interfaces** - Python API and CLI
- **Comprehensive validation** - Input validation with detailed error messages
- **Full test coverage** - 90%+ code coverage with extensive test suite

## Installation

```bash
pip install floating-base-converter
```

## API Reference

### BaseConverter

```python
from base_converter import BaseConverter

converter = BaseConverter(default_precision=10)
```

#### Core Methods

| Method | Description | Example |
|--------|-------------|---------|
| `decimal_to_binary(n, precision=None)` | Decimal → Binary | `3.14` → `"11.001001000011111101"` |
| `decimal_to_hex(n, precision=None)` | Decimal → Hexadecimal | `255.5` → `"FF.8"` |
| `binary_to_decimal(s, precision=None)` | Binary → Decimal | `"1010.01"` → `"10.25"` |
| `hex_to_decimal(s, precision=None)` | Hexadecimal → Decimal | `"A.8"` → `"10.5"` |
| `convert(n, from_base, to_base, precision=None)` | Universal converter | `("FF", 16, 2)` → `"11111111"` |

#### Input Types

- **Decimal**: `int`, `float`, or `str`
- **Non-decimal**: `str` only (e.g., `"1010.01"`, `"FF.8"`)

#### Supported Prefixes

- Binary: `0b1010` or `1010`
- Octal: `0o17` or `17`  
- Hexadecimal: `0xFF` or `FF`

### CLI Interface

```bash
base-converter <number> -f <from_base> -t <to_base> [-p <precision>]
```

#### Examples

```bash
# Decimal to hexadecimal
base-converter 3.14159 -f 10 -t 16 -p 6
# Output: 3.14159 (decimal) = 3.243F3E (hexadecimal)

# Binary to decimal  
base-converter "1010.01" -f 2 -t 10
# Output: 1010.01 (binary) = 10.25 (decimal)

# Hexadecimal to binary
base-converter "FF.8" -f 16 -t 2 -p 4
# Output: FF.8 (hexadecimal) = 11111111.1 (binary)
```

### Error Handling

```python
from base_converter import ConversionError

try:
    result = converter.binary_to_decimal("102")  # Invalid binary digit
except ConversionError as e:
    print(f"Error: {e}")
```

## Development

### Setup

```bash
git clone https://github.com/yeabwang/floating-base-converter.git
cd floating-base-converter
pip install -e ".[dev]"
```

### Testing

```bash
pytest                          # Run tests
pytest --cov=base_converter     # With coverage
```

### Code Quality

```bash
black base_converter tests/     # Format code
flake8 base_converter tests/    # Lint code  
mypy base_converter/           # Type checking
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Technical Specifications

- **Python**: 3.8+
- **Dependencies**: None (runtime)
- **Precision**: 1-50 fractional digits
- **Supported bases**: 2 (binary), 8 (octal), 10 (decimal), 16 (hexadecimal)
- **Performance**: O(n) conversion time, O(1) memory overhead
