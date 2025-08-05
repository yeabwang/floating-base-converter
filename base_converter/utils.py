from typing import Union
from decimal import Decimal


class ConversionError(Exception):
    """Custom exception for base conversion errors."""

    pass


def convert_scientific_notation(number_str: str) -> str:
    """
    Convert scientific notation to standard decimal format.

    Args:
        number_str: Number string that may contain scientific notation

    Returns:
        str: Standard decimal format

    Examples:
        "1.23e-4" -> "0.000123"
        "6.626e-34" -> "0.00000000000000000000000000000000006626"
        "1.23e+5" -> "123000"
    """
    # Check if it contains scientific notation
    if "e" not in number_str.lower():
        return number_str

    try:
        # Use Decimal for arbitrary precision scientific notation conversion
        decimal_value = Decimal(number_str)
        # Convert to string without scientific notation
        return format(decimal_value, "f")
    except Exception:
        # If Decimal fails, fall back to float (less precise but compatible)
        try:
            float_value = float(number_str)
            return f"{float_value:.50f}".rstrip("0").rstrip(".")
        except ValueError:
            raise ConversionError(f"Invalid scientific notation: {number_str}")


def normalize_input(number: Union[str, float, int], base: int) -> str:
    """
    Normalize input to a consistent string format.

    Args:
        number: Input number
        base: Base of the input number

    Returns:
        str: Normalized number string
    """
    if isinstance(number, (int, float)):
        if base == 10:
            return str(number)
        else:
            raise ConversionError(
                f"Numeric input only supported for decimal (base 10), got base {base}"
            )

    if isinstance(number, str):
        # Remove common prefixes
        number = number.strip()

        # Handle scientific notation for decimal base
        if base == 10 and ("e" in number.lower() or "E" in number):
            number = convert_scientific_notation(number)

        if base == 2 and number.lower().startswith("0b"):
            number = number[2:]
        elif base == 8 and number.lower().startswith("0o"):
            number = number[2:]
        elif base == 16 and number.lower().startswith("0x"):
            number = number[2:]

        return number.upper() if base == 16 else number

    raise ConversionError(f"Unsupported input type: {type(number)}")


def validate_input(number_str: str, base: int) -> None:
    """
    Validate input string for the given base.

    Args:
        number_str: Number string to validate
        base: Base to validate against

    Raises:
        ConversionError: If input is invalid
    """
    if not number_str:
        raise ConversionError("Empty input")

    # Check for valid characters based on base
    valid_chars = {
        2: set("01.-"),
        8: set("01234567.-"),
        10: set("0123456789.-"),
        16: set("0123456789ABCDEF.-"),
    }

    if base not in valid_chars:
        raise ConversionError(f"Unsupported base: {base}")

    # Remove negative sign for validation
    check_str = number_str[1:] if number_str.startswith("-") else number_str

    # Check for invalid characters
    for char in check_str:
        if char not in valid_chars[base]:
            raise ConversionError(f"Invalid character '{char}' for base {base}")

    # Check for multiple decimal points
    if check_str.count(".") > 1:
        raise ConversionError("Multiple decimal points found")

    # Check for empty parts
    if check_str.startswith(".") or check_str.endswith("."):
        if check_str in [".", "-."]:
            raise ConversionError("Invalid number format")
