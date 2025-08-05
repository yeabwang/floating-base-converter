from typing import Union, Tuple, Optional
from decimal import Decimal, getcontext
from .utils import validate_input, normalize_input, ConversionError


class BaseConverter:
    """
    A class for converting floating-point numbers between different bases.

    Supports conversion between decimal (base 10), binary (base 2),
    octal (base 8), and hexadecimal (base 16).
    """

    def __init__(self, default_precision: int = 10):
        """
        Initialize the BaseConverter.

        Args:
            default_precision (int): Default precision for fractional part conversion.
                                   Must be between 1 and 100.
        """
        if not isinstance(default_precision, int) or not (
            1 <= default_precision <= 100
        ):
            raise ConversionError(
                "Default precision must be an integer between 1 and 100"
            )

        self.default_precision = default_precision
        self.hex_digits = "0123456789ABCDEF"

        # Set decimal precision high enough for calculations
        getcontext().prec = max(default_precision + 20, 50)

    def _split_number(self, num_str: str, base: int) -> Tuple[str, str]:
        """Split a number string into integer and fractional parts."""
        if "." in num_str:
            integer_part, fractional_part = num_str.split(".", 1)
        else:
            integer_part, fractional_part = num_str, ""

        return integer_part, fractional_part

    def _convert_integer_part(
        self, integer_str: str, from_base: int, to_base: int
    ) -> str:
        """Convert integer part between bases."""
        if not integer_str or integer_str == "0":
            return "0"

        # Convert to decimal first
        decimal_value = int(integer_str, from_base)

        if to_base == 10:
            return str(decimal_value)
        elif to_base == 2:
            return bin(decimal_value)[2:]
        elif to_base == 8:
            return oct(decimal_value)[2:]
        elif to_base == 16:
            return hex(decimal_value)[2:].upper()
        else:
            raise ConversionError(f"Unsupported base: {to_base}")

    def _convert_fractional_part(
        self, fractional_str: str, from_base: int, to_base: int, precision: int
    ) -> str:
        """Convert fractional part between bases using high-precision arithmetic."""
        if not fractional_str:
            return ""

        # Set decimal precision high enough for calculations
        original_prec = getcontext().prec
        getcontext().prec = max(precision + 50, 100)

        try:
            # Convert fractional part to decimal using Decimal for arbitrary precision
            decimal_fraction = Decimal(0)
            base_decimal = Decimal(from_base)

            for i, digit in enumerate(fractional_str):
                if digit.upper() in self.hex_digits:
                    digit_value = self.hex_digits.index(digit.upper())
                    if digit_value >= from_base:
                        raise ConversionError(
                            f"Invalid digit '{digit}' for base {from_base}"
                        )
                    # Use Decimal arithmetic for precision
                    decimal_fraction += Decimal(digit_value) * (
                        base_decimal ** -(i + 1)
                    )
                else:
                    raise ConversionError(f"Invalid digit '{digit}'")

            if to_base == 10:
                # For decimal, format with appropriate precision
                result_str = (
                    str(decimal_fraction).split(".")[1]
                    if "." in str(decimal_fraction)
                    else "0"
                )
                # Limit to requested precision
                result_str = result_str[:precision].rstrip("0")
                return result_str if result_str else "0"

            # Convert decimal fraction to target base using Decimal arithmetic
            result_list = []
            current_fraction = decimal_fraction
            to_base_decimal = Decimal(to_base)

            for _ in range(precision):
                if current_fraction == 0:
                    break

                current_fraction *= to_base_decimal
                result_digit: int = int(current_fraction)

                if to_base == 16:
                    result_list.append(self.hex_digits[result_digit])
                else:
                    result_list.append(str(result_digit))

                current_fraction -= Decimal(result_digit)

            return "".join(result_list)

        finally:
            # Restore original precision
            getcontext().prec = original_prec

    def _convert_base(
        self,
        number: Union[str, float],
        from_base: int,
        to_base: int,
        precision: Optional[int] = None,
    ) -> str:
        """General base conversion method."""
        if precision is None:
            precision = self.default_precision

        if not isinstance(precision, int) or not (1 <= precision <= 100):
            raise ConversionError("Precision must be an integer between 1 and 100")

        # Set decimal precision high enough for calculations
        original_prec = getcontext().prec
        getcontext().prec = max(precision + 20, 50)

        try:
            # Normalize and validate input
            number_str = normalize_input(number, from_base)
            validate_input(number_str, from_base)

            # Handle negative numbers
            is_negative = number_str.startswith("-")
            if is_negative:
                number_str = number_str[1:]

            # Split into integer and fractional parts
            integer_part, fractional_part = self._split_number(number_str, from_base)

            # Convert parts
            converted_integer = self._convert_integer_part(
                integer_part, from_base, to_base
            )
            converted_fractional = self._convert_fractional_part(
                fractional_part, from_base, to_base, precision
            )

            # Combine result
            if converted_fractional and converted_fractional != "0":
                result = f"{converted_integer}.{converted_fractional}"
            else:
                result = converted_integer

            if is_negative:
                result = f"-{result}"

            return result

        finally:
            # Restore original precision
            getcontext().prec = original_prec

    # Decimal conversions
    def decimal_to_binary(
        self, number: Union[str, float], precision: Optional[int] = None
    ) -> str:
        """Convert decimal to binary."""
        return self._convert_base(number, 10, 2, precision)

    def decimal_to_octal(
        self, number: Union[str, float], precision: Optional[int] = None
    ) -> str:
        """Convert decimal to octal."""
        return self._convert_base(number, 10, 8, precision)

    def decimal_to_hex(
        self, number: Union[str, float], precision: Optional[int] = None
    ) -> str:
        """Convert decimal to hexadecimal."""
        return self._convert_base(number, 10, 16, precision)

    # Binary conversions
    def binary_to_decimal(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert binary to decimal."""
        return self._convert_base(number, 2, 10, precision)

    def binary_to_octal(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert binary to octal."""
        return self._convert_base(number, 2, 8, precision)

    def binary_to_hex(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert binary to hexadecimal."""
        return self._convert_base(number, 2, 16, precision)

    # Octal conversions
    def octal_to_decimal(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert octal to decimal."""
        return self._convert_base(number, 8, 10, precision)

    def octal_to_binary(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert octal to binary."""
        return self._convert_base(number, 8, 2, precision)

    def octal_to_hex(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert octal to hexadecimal."""
        return self._convert_base(number, 8, 16, precision)

    # Hexadecimal conversions
    def hex_to_decimal(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert hexadecimal to decimal."""
        return self._convert_base(number, 16, 10, precision)

    def hex_to_binary(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert hexadecimal to binary."""
        return self._convert_base(number, 16, 2, precision)

    def hex_to_octal(
        self, number: Union[str, int], precision: Optional[int] = None
    ) -> str:
        """Convert hexadecimal to octal."""
        return self._convert_base(number, 16, 8, precision)

    # Universal converter
    def convert(
        self,
        number: Union[str, float],
        from_base: int,
        to_base: int,
        precision: Optional[int] = None,
    ) -> str:
        """
        Universal conversion method.

        Args:
            number: Number to convert (string or float)
            from_base: Source base (2, 8, 10, or 16)
            to_base: Target base (2, 8, 10, or 16)
            precision: Decimal precision for fractional part

        Returns:
            str: Converted number as string
        """
        supported_bases = [2, 8, 10, 16]
        if from_base not in supported_bases or to_base not in supported_bases:
            raise ConversionError(f"Supported bases are: {supported_bases}")

        return self._convert_base(number, from_base, to_base, precision)
