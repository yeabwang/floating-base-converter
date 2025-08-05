import pytest
from base_converter.utils import validate_input, normalize_input
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