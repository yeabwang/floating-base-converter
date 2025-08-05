import pytest
from base_converter import BaseConverter, ConversionError


class TestBaseConverter:
    """Test cases for BaseConverter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.converter = BaseConverter()

    def test_decimal_to_binary(self):
        """Test decimal to binary conversion."""
        assert self.converter.decimal_to_binary(5) == "101"
        assert self.converter.decimal_to_binary(3.5) == "11.1"
        assert self.converter.decimal_to_binary("10.25") == "1010.01"
        assert self.converter.decimal_to_binary(0) == "0"

    def test_decimal_to_hex(self):
        """Test decimal to hexadecimal conversion."""
        assert self.converter.decimal_to_hex(255) == "FF"
        assert self.converter.decimal_to_hex(15.9375) == "F.F"
        assert self.converter.decimal_to_hex("10.5") == "A.8"

    def test_decimal_to_octal(self):
        """Test decimal to octal conversion."""
        assert self.converter.decimal_to_octal(8) == "10"
        assert self.converter.decimal_to_octal(8.75, precision=1) == "10.6"

    def test_binary_to_decimal(self):
        """Test binary to decimal conversion."""
        assert self.converter.binary_to_decimal("101") == "5"
        assert self.converter.binary_to_decimal("11.1") == "3.5"
        assert self.converter.binary_to_decimal("1010.01") == "10.25"

    def test_hex_to_decimal(self):
        """Test hexadecimal to decimal conversion."""
        assert self.converter.hex_to_decimal("FF") == "255"
        assert self.converter.hex_to_decimal("A.8") == "10.5"
        assert self.converter.hex_to_decimal("0xFF") == "255"  # With prefix

    def test_octal_to_decimal(self):
        """Test octal to decimal conversion."""
        assert self.converter.octal_to_decimal("10") == "8"
        assert self.converter.octal_to_decimal("10.6") == "8.75"

    def test_precision_parameter(self):
        """Test precision parameter."""
        result = self.converter.decimal_to_binary(0.1, precision=5)
        fractional_part = result.split(".")[1] if "." in result else ""
        assert len(fractional_part) <= 5

    def test_negative_numbers(self):
        """Test negative number conversion."""
        assert self.converter.decimal_to_binary(-5) == "-101"
        assert self.converter.binary_to_decimal("-101") == "-5"
        assert self.converter.decimal_to_hex(-10) == "-A"

    def test_zero_conversion(self):
        """Test zero conversion."""
        assert self.converter.decimal_to_binary(0) == "0"
        assert self.converter.binary_to_decimal("0") == "0"
        assert self.converter.decimal_to_hex(0) == "0"

    def test_invalid_input(self):
        """Test invalid input handling."""
        with pytest.raises(ConversionError):
            self.converter.binary_to_decimal("102")  # Invalid binary digit

        with pytest.raises(ConversionError):
            self.converter.hex_to_decimal("XYZ")  # Invalid hex digits

        with pytest.raises(ConversionError):
            self.converter.octal_to_decimal("89")  # Invalid octal digits

    def test_invalid_precision(self):
        """Test invalid precision handling."""
        with pytest.raises(ConversionError):
            BaseConverter(default_precision=0)

        with pytest.raises(ConversionError):
            BaseConverter(default_precision=51)

        with pytest.raises(ConversionError):
            self.converter.decimal_to_binary(3.14, precision=51)

    def test_universal_converter(self):
        """Test universal convert method."""
        assert self.converter.convert(10, 10, 2) == "1010"
        assert self.converter.convert("FF", 16, 10) == "255"
        assert self.converter.convert("101", 2, 8) == "5"
        assert self.converter.convert("10.5", 10, 16) == "A.8"

    def test_edge_cases(self):
        """Test edge cases."""
        # Empty fractional part
        assert self.converter.decimal_to_binary("5.") == "101"

        # Large numbers
        assert self.converter.decimal_to_hex(4095) == "FFF"

        # Very small fractions
        result = self.converter.decimal_to_binary(0.0625, precision=4)
        assert result == "0.0001"

    def test_cross_conversions(self):
        """Test conversions between all bases."""
        # Test a round trip
        original = "10.5"
        hex_result = self.converter.decimal_to_hex(original)
        back_to_decimal = self.converter.hex_to_decimal(hex_result)
        assert back_to_decimal == "10.5"

        # Binary to octal
        assert self.converter.binary_to_octal("1010") == "12"

        # Octal to hex
        assert self.converter.octal_to_hex("17") == "F"
