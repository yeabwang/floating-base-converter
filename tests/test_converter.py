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
            BaseConverter(default_precision=101)

        with pytest.raises(ConversionError):
            self.converter.decimal_to_binary(3.14, precision=101)

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

    def test_high_precision_conversions(self):
        """Test high precision conversions (51-100 digits)."""
        # Test with 60 digits precision
        pi_60_digits = "3.141592653589793238462643383279502884197169399375105820974944"
        
        # Convert to hex with 60 digits precision
        hex_result = self.converter.decimal_to_hex(pi_60_digits, precision=60)
        assert len(hex_result.split('.')[1]) <= 60
        assert hex_result.startswith("3.243F6A8885A308D313198A2E03707344A4093822299F31D0")
        
        # Test with 80 digits precision
        binary_result = self.converter.decimal_to_binary("1.5", precision=80)
        assert binary_result == "1.1"  # Simple test that still works
        
        # Test that precision=100 works
        octal_result = self.converter.decimal_to_octal("0.125", precision=100)
        assert octal_result == "0.1"

    def test_decimal_precision_accuracy(self):
        """Test that decimal arithmetic provides better accuracy than float."""
        # Test a number that requires high precision
        test_number = "1.23456789012345678901234567890123456789012345678901234567890"
        
        # Convert with high precision
        hex_result = self.converter.decimal_to_hex(test_number, precision=70)
        
        # Should maintain precision better than float-based approach
        assert len(hex_result.split('.')[1]) > 50  # More than old limit
        assert hex_result.startswith("1.3C0CA428C59FB71A7B")  # Verify accuracy

    def test_scientific_notation_support(self):
        """Test scientific notation input support."""
        # Basic scientific notation conversions
        result = self.converter.decimal_to_hex("1.23e-4", precision=10)
        expected = self.converter.decimal_to_hex("0.000123", precision=10)
        assert result == expected
        
        # Large exponents
        result = self.converter.decimal_to_binary("1e3")
        expected = self.converter.decimal_to_binary("1000")
        assert result == expected
        
        # Negative exponents with high precision
        result = self.converter.decimal_to_hex("6.626e-34", precision=50)
        assert result.startswith("0.")
        assert len(result.split('.')[1]) > 30  # Should have many fractional digits
        
        # Positive exponents
        result = self.converter.decimal_to_octal("1.23e2", precision=5)
        expected = self.converter.decimal_to_octal("123", precision=5)
        assert result == expected
        
        # Case insensitive
        result1 = self.converter.decimal_to_hex("1.5e-3", precision=10)
        result2 = self.converter.decimal_to_hex("1.5E-3", precision=10)
        assert result1 == result2

    def test_scientific_notation_edge_cases(self):
        """Test edge cases for scientific notation."""
        # Zero exponent
        result = self.converter.decimal_to_hex("1.5e0")
        expected = self.converter.decimal_to_hex("1.5")
        assert result == expected
        
        # Very small numbers
        result = self.converter.decimal_to_binary("1e-10", precision=40)
        assert result.startswith("0.")
        
        # Very large numbers  
        result = self.converter.decimal_to_hex("1e10")
        assert result == "2540BE400"  # 10 billion in hex

    def test_scientific_notation_validation_errors(self):
        """Test that scientific notation is properly validated for different bases."""
        # Scientific notation should only work for decimal base
        with pytest.raises(ConversionError):
            self.converter.binary_to_decimal("1.23e-4")  # 'e' invalid in binary
            
        with pytest.raises(ConversionError):
            self.converter.convert("1e5", 2, 10)  # 'e' invalid in binary source
