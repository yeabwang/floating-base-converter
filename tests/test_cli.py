import pytest
import sys
from unittest.mock import patch
from base_converter.cli import main


class TestCLI:
    """Test command-line interface."""

    def test_basic_conversion(self, capsys):
        """Test basic CLI conversion."""
        with patch.object(sys, "argv", ["base-converter", "10", "-f", "10", "-t", "2"]):
            main()
            captured = capsys.readouterr()
            assert "10 (decimal) = 1010 (binary)" in captured.out

    def test_hex_conversion(self, capsys):
        """Test hexadecimal conversion."""
        with patch.object(
            sys, "argv", ["base-converter", "FF", "-f", "16", "-t", "10"]
        ):
            main()
            captured = capsys.readouterr()
            assert "FF (hexadecimal) = 255 (decimal)" in captured.out

    def test_precision_parameter(self, capsys):
        """Test precision parameter."""
        with patch.object(
            sys, "argv", ["base-converter", "3.14159", "-f", "10", "-t", "2", "-p", "5"]
        ):
            main()
            captured = capsys.readouterr()
            assert "3.14159 (decimal)" in captured.out
            assert "(binary)" in captured.out

    def test_invalid_input(self, capsys):
        """Test invalid input handling."""
        with patch.object(
            sys, "argv", ["base-converter", "102", "-f", "2", "-t", "10"]
        ):
            with pytest.raises(SystemExit):
                main()
            captured = capsys.readouterr()
            assert "Error:" in captured.err
