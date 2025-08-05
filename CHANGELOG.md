# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-08-05

### Added
- **100-digit precision support** - Upgraded from 50 to 100 fractional digits
- **Scientific notation support** - Full exponential notation parsing (1.23e-4, 6.626E-34, etc.)
- **Decimal arithmetic engine** - Replaced float with Decimal for enhanced precision and performance
- **Enhanced testing suite** - Expanded from 22 to 30 tests with 91% code coverage
- **Performance benchmarking** - Comprehensive performance analysis and validation
- **Real-world examples** - Scientific, financial, and engineering use cases
- **Scientific notation validation** - Base-specific validation for exponential notation
- **High-precision mathematical constants** - π, e, √2, golden ratio with 100-digit precision

### Enhanced
- **Performance improvements** - 1.4-5x faster conversions using Decimal arithmetic
- **Memory efficiency** - Constant ~2.6KB memory usage across all precision levels
- **Error handling** - Enhanced validation for scientific notation and high precision
- **Documentation** - Comprehensive technical documentation with performance tables
- **API stability** - Backward compatible with all existing functionality

### Technical
- Decimal module integration for arbitrary precision arithmetic
- Scientific notation parser with comprehensive validation
- Enhanced input normalization supporting exponential notation
- Performance optimization for sub-millisecond conversions
- Comprehensive benchmark suite with accuracy verification
- Enhanced demo scripts showcasing practical applications

### Breaking Changes
- None - Full backward compatibility maintained

### Performance
- Sub-millisecond conversions at 100-digit precision
- 1.4-5x performance improvement over float arithmetic
- Memory usage remains constant at ~2.6KB regardless of precision
- Scientific notation processing with minimal overhead

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
