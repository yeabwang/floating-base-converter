# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-08-05

### Added
- Initial release of floating-base-converter
- Support for converting floating-point numbers between decimal, binary, octal, and hexadecimal bases
- Command-line interface with `base-converter` command
- Python API with `BaseConverter` class
- Comprehensive test suite with 90%+ coverage
- Input validation and error handling
- Support for custom precision in conversions

### Features
- Decimal ↔ Binary conversions
- Decimal ↔ Octal conversions  
- Decimal ↔ Hexadecimal conversions
- Cross-base conversions (e.g., Binary ↔ Hexadecimal)
- Floating-point number support
- Negative number support
- CLI with intuitive arguments
- Comprehensive error messages

### Technical
- Python 3.8+ support
- Zero runtime dependencies
- Modern project structure with pyproject.toml
- Code quality tools (black, flake8, pytest)
- Type hints throughout codebase
