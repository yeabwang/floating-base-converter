import pytest
from base_converter.utils import (
    validate_input,
    normalize_input,
    convert_scientific_notation,
)
from base_converter import ConversionError


class TestUtils:
    """Test utility functions."""

    def test_normalize_input(self):
        """Test input normalization."""
        assert normalize_input("0xFF", 16) == "FF"
        assert normalize_input("0b101", 2) == "101"
        assert normalize_input("0o17", 8) == "17"
        assert normalize_input(10.5, 10) == "10.5"
        assert normalize_input("  FF  ", 16) == "FF"

    def test_normalize_input_errors(self):
        """Test normalization error cases."""
        with pytest.raises(ConversionError):
            normalize_input(10, 2)  # Numeric input for non-decimal base

        with pytest.raises(ConversionError):
            normalize_input([], 10)  # type: ignore # Invalid type

    def test_validate_input(self):
        """Test input validation."""
        # Valid inputs
        validate_input("101", 2)
        validate_input("17.6", 8)
        validate_input("FF.A", 16)
        validate_input("-10.5", 10)

        # Should not raise exceptions
        assert True

    def test_validate_input_errors(self):
        """Test validation error cases."""
        with pytest.raises(ConversionError):
            validate_input("", 10)  # Empty input

        with pytest.raises(ConversionError):
            validate_input("102", 2)  # Invalid binary digit

        with pytest.raises(ConversionError):
            validate_input("89", 8)  # Invalid octal digit

        with pytest.raises(ConversionError):
            validate_input("XYZ", 16)  # Invalid hex digits

        with pytest.raises(ConversionError):
            validate_input("10.5.3", 10)  # Multiple decimals

        with pytest.raises(ConversionError):
            validate_input(".", 10)  # Just decimal point

    def test_scientific_notation_conversion(self):
        """Test scientific notation conversion."""
        # Basic scientific notation
        assert convert_scientific_notation("1.23e2") == "123"
        assert convert_scientific_notation("1.23e-2") == "0.0123"
        assert convert_scientific_notation("1.23E+2") == "123"
        assert convert_scientific_notation("1.23E-2") == "0.0123"

        # Large numbers
        assert convert_scientific_notation("6.626e-34").startswith(
            "0.000000000000000000000000000000000"
        )
        assert convert_scientific_notation("1.23e20") == "123000000000000000000"

        # Non-scientific notation should pass through
        assert convert_scientific_notation("123.456") == "123.456"
        assert convert_scientific_notation("0.001") == "0.001"

        # Edge cases
        assert convert_scientific_notation("1e0") == "1"
        assert convert_scientific_notation("1e1") == "10"
        assert convert_scientific_notation("1e-1") == "0.1"

    def test_scientific_notation_in_normalize_input(self):
        """Test scientific notation handling in normalize_input."""
        # Scientific notation should be converted for decimal base
        assert normalize_input("1.23e-4", 10) == "0.000123"
        assert normalize_input("6.626E-34", 10).startswith(
            "0.000000000000000000000000000000000"
        )
        assert normalize_input("1.23e+5", 10) == "123000"

        # Should work with whitespace
        assert normalize_input("  1.23e-4  ", 10) == "0.000123"

        # Non-decimal bases should NOT convert scientific notation (leave as-is)
        # The validation will catch invalid characters later
        assert normalize_input("1.23e-4", 2) == "1.23e-4"  # Not converted

    def test_scientific_notation_errors(self):
        """Test error handling for invalid scientific notation."""
        with pytest.raises(ConversionError):
            convert_scientific_notation("1.23ee-4")  # Double e

        with pytest.raises(ConversionError):
            convert_scientific_notation("e-4")  # Missing mantissa
