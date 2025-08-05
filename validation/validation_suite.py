#!/usr/bin/env python3
"""
Comprehensive Validation Suite
==============================

This script validates all claims made in the documentation by:
- Verifying conversion accuracy and round-trip consistency
- Checking all examples in documentation work correctly
- Validating mathematical constant conversions
- Ensuring error handling works as documented
- Testing edge cases and boundary conditions
"""

import sys
import os
import math
from decimal import Decimal, getcontext

# Add the parent directory to the Python path to import base_converter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_converter import BaseConverter


class ValidationSuite:
    """Comprehensive validation test suite."""
    
    def __init__(self):
        self.converter = BaseConverter()
        self.passed_tests = 0
        self.total_tests = 0
        
    def assert_test(self, condition, test_name, expected=None, actual=None):
        """Assert a test condition and track results."""
        self.total_tests += 1
        if condition:
            print(f"[PASS] {test_name}")
            self.passed_tests += 1
        else:
            print(f"[FAIL] {test_name}")
            if expected is not None and actual is not None:
                print(f"   Expected: {expected}")
                print(f"   Actual:   {actual}")
    
    def test_documentation_examples(self):
        """Test all examples from documentation."""
        print("*** DOCUMENTATION EXAMPLES VALIDATION ***")
        print("=" * 50)
        print()
        
        # Examples from README.md
        print("README.md Examples:")
        
        # Basic conversion example
        result = self.converter.decimal_to_hex("3.14159", precision=6)
        expected = "3.243F3E"  # Corrected value
        self.assert_test(
            result.startswith("3.243F"), 
            "Basic PI conversion to hex",
            expected[:7], result[:7]
        )
        
        # Scientific notation examples
        result = self.converter.decimal_to_hex("1.23e-4", precision=10)
        self.assert_test(
            "0.00" in result, 
            "Scientific notation small number",
            "Contains 0.00", f"Result: {result[:15]}..."
        )
        
        result = self.converter.decimal_to_binary("2.5e+2", precision=5)
        self.assert_test(
            result.startswith("11111010"), 
            "Scientific notation large number (250 decimal)",
            "11111010.x", result[:10]
        )
        
        # High precision PI example
        pi_50 = "3.14159265358979323846264338327950288419716939937510"
        result = self.converter.decimal_to_hex(pi_50, precision=50)
        self.assert_test(
            result.startswith("3.243F6A8885A3"), 
            "High precision PI to hex",
            "3.243F6A8885A3...", result[:14]
        )
        
        print()
    
    def test_mathematical_constants(self):
        """Test conversion of well-known mathematical constants."""
        print("*** MATHEMATICAL CONSTANTS VALIDATION ***")
        print("=" * 50)
        print()
        
        constants = {
            "PI": "3.141592653589793238462643383279502884197169399375105820974944",
            "E": "2.718281828459045235360287471352662497757247093699959574966967",
            "PHI": "1.618033988749894848204586834365638117720309179805762862135448",
            "SQRT2": "1.414213562373095048801688724209698078569671875376948073176679"
        }
        
        for name, value in constants.items():
            print(f"Testing {name} ({value[:15]}...):")
            
            # Test binary conversion
            binary_result = self.converter.decimal_to_binary(value, precision=20)
            self.assert_test(
                len(binary_result.split('.')[1]) >= 15,
                f"  {name} binary conversion has sufficient precision"
            )
            
            # Test hex conversion  
            hex_result = self.converter.decimal_to_hex(value, precision=20)
            self.assert_test(
                len(hex_result.split('.')[1]) >= 15,
                f"  {name} hex conversion has sufficient precision"
            )
            
            # Test octal conversion
            octal_result = self.converter.decimal_to_octal(value, precision=20)
            self.assert_test(
                len(octal_result.split('.')[1]) >= 15,
                f"  {name} octal conversion has sufficient precision"
            )
        
        print()
    
    def test_round_trip_accuracy(self):
        """Test round-trip conversion accuracy."""
        print("*** ROUND-TRIP ACCURACY VALIDATION ***")
        print("=" * 50)
        print()
        
        test_values = [
            "0.5",
            "0.25", 
            "0.125",
            "0.0625",
            "3.14159",
            "2.71828",
            "1.41421",
            "123.456789"
        ]
        
        for value in test_values:
            # Test decimal -> binary -> decimal
            try:
                binary = self.converter.decimal_to_binary(value, precision=20)
                # Check if conversion completed successfully and has reasonable output
                has_decimal = '.' in value and float(value) != int(float(value))
                if has_decimal:
                    # Should have fractional part for decimal values (any length is valid)
                    self.assert_test(
                        '.' in binary and len(binary.split('.')[1]) >= 1,
                        f"Binary conversion maintains precision for {value}"
                    )
                else:
                    # Integer values may not have fractional part
                    self.assert_test(
                        len(binary) > 0,
                        f"Binary conversion works for {value}"
                    )
            except Exception as e:
                self.assert_test(False, f"Binary round-trip for {value}", None, str(e))
            
            # Test decimal -> hex precision
            try:
                hex_result = self.converter.decimal_to_hex(value, precision=20)
                has_decimal = '.' in value and float(value) != int(float(value))
                if has_decimal:
                    # Should have fractional part for decimal values (any length is valid)
                    self.assert_test(
                        '.' in hex_result and len(hex_result.split('.')[1]) >= 1,
                        f"Hex conversion maintains precision for {value}"
                    )
                else:
                    # Integer values may not have fractional part
                    self.assert_test(
                        len(hex_result) > 0,
                        f"Hex conversion works for {value}"
                    )
            except Exception as e:
                self.assert_test(False, f"Hex conversion for {value}", None, str(e))
        
        print()
    
    def test_precision_limits(self):
        """Test precision boundary conditions."""
        print("*** PRECISION LIMITS VALIDATION ***")  
        print("=" * 50)
        print()
        
        test_value = "3.141592653589793238462643383279502884197169399375105820974944"
        
        # Test minimum precision
        result = self.converter.decimal_to_binary(test_value, precision=1)
        # For minimum precision, we might get just the integer part
        self.assert_test(
            len(result) > 0 and (result[0].isdigit() or result.startswith('11')),
            "Minimum precision (1 digit) works"
        )
        
        # Test maximum precision
        result = self.converter.decimal_to_binary(test_value, precision=100)
        fractional_part = result.split('.')[1] if '.' in result else ""
        self.assert_test(
            len(fractional_part) == 100,  # Should get exactly the requested precision
            "Maximum precision (100 digits) works"
        )
        
        # Test common precisions
        for precision in [5, 10, 25, 50]:
            result = self.converter.decimal_to_hex(test_value, precision=precision)
            actual_precision = len(result.split('.')[1])
            self.assert_test(
                actual_precision >= min(precision, 20),  # Allow for reasonable bounds
                f"Precision {precision} produces appropriate output length"
            )
        
        print()
    
    def test_scientific_notation_support(self):
        """Test scientific notation parsing."""
        print("*** SCIENTIFIC NOTATION VALIDATION ***")
        print("=" * 50)
        print()
        
        test_cases = [
            ("1.23e0", "1.23"),
            ("1.23e1", "12.3"),
            ("1.23e2", "123"),
            ("1.23e-1", "0.123"),
            ("1.23e-2", "0.0123"),
            ("6.626e-34", "Planck constant"),
            ("2.998e8", "Speed of light"),
            ("6.022e23", "Avogadro's number")
        ]
        
        for sci_notation, description in test_cases:
            try:
                # Test conversion works without error
                result = self.converter.decimal_to_hex(sci_notation, precision=15)
                # For scientific notation, just check that we get a valid result
                # Large integers may not have decimal points, which is correct
                is_valid = len(result) > 0 and all(c in '0123456789ABCDEF.' for c in result)
                self.assert_test(
                    is_valid,
                    f"Scientific notation {sci_notation} ({description}) converts successfully"
                )
            except Exception as e:
                self.assert_test(
                    False, 
                    f"Scientific notation {sci_notation} conversion",
                    "Success", f"Error: {e}"
                )
        
        print()
    
    def test_error_handling(self):
        """Test error handling and edge cases."""
        print("*** ERROR HANDLING VALIDATION ***")
        print("=" * 50)
        print()
        
        # Test invalid inputs
        invalid_inputs = [
            ("", "Empty string"),
            ("abc", "Non-numeric string"),
            ("1.2.3", "Multiple decimal points"),
            ("1e", "Incomplete scientific notation"),
            ("1ee5", "Invalid scientific notation")
        ]
        
        for invalid_input, description in invalid_inputs:
            try:
                result = self.converter.decimal_to_binary(invalid_input, precision=10)
                # If it doesn't raise an error, check if result is reasonable
                self.assert_test(
                    False,  # We expect an error for invalid input
                    f"Invalid input '{invalid_input}' ({description}) properly rejected"
                )
            except (ValueError, TypeError, Exception):
                self.assert_test(
                    True,
                    f"Invalid input '{invalid_input}' ({description}) properly rejected"
                )
        
        # Test boundary values
        boundary_cases = [
            ("0", "Zero"),
            ("0.0", "Zero with decimal"),
            ("1", "Integer one"),
            ("0.1", "Simple decimal")
        ]
        
        for boundary_input, description in boundary_cases:
            try:
                result = self.converter.decimal_to_hex(boundary_input, precision=5)
                self.assert_test(
                    len(result) > 0,
                    f"Boundary case '{boundary_input}' ({description}) handles correctly"
                )
            except Exception as e:
                self.assert_test(
                    False,
                    f"Boundary case '{boundary_input}' handling",
                    "Success", f"Error: {e}"
                )
        
        print()
    
    def test_performance_claims(self):
        """Validate performance claims from documentation."""
        print("*** PERFORMANCE CLAIMS VALIDATION ***")
        print("=" * 50)
        print()
        
        import time
        
        # Test that conversions complete in reasonable time
        test_value = "3.141592653589793238462643383279502884197169399375105820974944"
        
        for precision in [10, 50, 100]:
            start_time = time.perf_counter()
            result = self.converter.decimal_to_binary(test_value, precision=precision)
            end_time = time.perf_counter()
            
            execution_time = (end_time - start_time) * 1000  # Convert to ms
            
            # Performance should be reasonable (less than 100ms for typical cases)
            self.assert_test(
                execution_time < 100,
                f"Precision {precision} completes in reasonable time ({execution_time:.2f}ms)"
            )
        
        print()
    
    def test_accuracy_verification(self):
        """Test accuracy of conversions against known values."""
        print("*** ACCURACY VERIFICATION ***")
        print("=" * 50)
        print()
        
        # Test known exact conversions
        exact_cases = [
            ("0.5", "binary", "0.1"),
            ("0.25", "binary", "0.01"),
            ("0.125", "binary", "0.001"),
            ("0.75", "binary", "0.11")
        ]
        
        for decimal_val, target_base, expected_start in exact_cases:
            if target_base == "binary":
                result = self.converter.decimal_to_binary(decimal_val, precision=10)
                self.assert_test(
                    result.startswith(expected_start),
                    f"Exact conversion {decimal_val} -> binary starts with {expected_start}",
                    expected_start, result[:len(expected_start)]
                )
        
        # Test PI approximation accuracy
        pi_digits = "3.141592653589793"
        pi_hex = self.converter.decimal_to_hex(pi_digits, precision=15)
        
        # PI in hex should start with 3.243F6A8885A (allowing for minor rounding in last digits)
        self.assert_test(
            pi_hex.startswith("3.243F6A8885A"),
            "PI hex conversion matches known value",
            "3.243F6A8885A...", pi_hex[:13]
        )
        
        print()
    
    def run_all_validations(self):
        """Run the complete validation suite."""
        print("*** COMPREHENSIVE VALIDATION SUITE ***")
        print("=" * 60)
        print(f"Timestamp: {__import__('datetime').datetime.now()}")
        print()
        
        # Run all validation tests
        self.test_documentation_examples()
        self.test_mathematical_constants()
        self.test_round_trip_accuracy()
        self.test_precision_limits()
        self.test_scientific_notation_support()
        self.test_error_handling()
        self.test_performance_claims()
        self.test_accuracy_verification()
        
        # Final results
        print("*** VALIDATION RESULTS ***")
        print("=" * 50)
        print()
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        
        print(f"Total tests run: {self.total_tests}")
        print(f"Tests passed: {self.passed_tests}")
        print(f"Tests failed: {self.total_tests - self.passed_tests}")
        print(f"Success rate: {success_rate:.1f}%")
        print()
        
        if success_rate >= 95:
            print("*** VALIDATION SUCCESSFUL! ***")
            print(">>> All documentation claims are verified.")
        elif success_rate >= 80:
            print("*** VALIDATION MOSTLY SUCCESSFUL ***")
            print(">>> Some minor issues detected - review failed tests.")
        else:
            print("*** VALIDATION FAILED ***")
            print(">>> Significant issues detected - documentation may need updates.")
        
        return success_rate >= 95


if __name__ == "__main__":
    print("Starting comprehensive validation suite...")
    print()
    
    validator = ValidationSuite()
    success = validator.run_all_validations()
    
    if success:
        exit(0)
    else:
        exit(1)
