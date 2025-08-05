from base_converter import BaseConverter

def test_package():
    converter = BaseConverter()
    
    print("=== Manual Tests ===")
    print(f"Decimal to Binary: 3.14159 -> {converter.decimal_to_binary(3.14159, 10)}")
    print(f"Decimal to Hex: 255.75 -> {converter.decimal_to_hex(255.75)}")
    print(f"Binary to Decimal: 1010.01 -> {converter.binary_to_decimal('1010.01')}")
    print(f"Hex to Binary: FF.8 -> {converter.hex_to_binary('FF.8')}")
    print(f"Universal: FF (hex) to binary -> {converter.convert('FF', 16, 2)}")

if __name__ == "__main__":
    test_package()