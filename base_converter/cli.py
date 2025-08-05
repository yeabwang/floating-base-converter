import argparse
import sys
from .converter import BaseConverter, ConversionError


def main():
    """Command-line interface for the base converter."""
    parser = argparse.ArgumentParser(
        description="Convert floating-point numbers between different bases",
        epilog="Example: base-converter 3.14159 -f 10 -t 16 -p 6",
    )

    parser.add_argument("number", help="Number to convert")
    parser.add_argument(
        "--from-base",
        "-f",
        type=int,
        choices=[2, 8, 10, 16],
        default=10,
        help="Source base (default: 10)",
    )
    parser.add_argument(
        "--to-base",
        "-t",
        type=int,
        choices=[2, 8, 10, 16],
        default=2,
        help="Target base (default: 2)",
    )
    parser.add_argument(
        "--precision",
        "-p",
        type=int,
        default=10,
        help="Precision for fractional part (default: 10)",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    try:
        converter = BaseConverter(default_precision=args.precision)
        result = converter.convert(
            args.number, args.from_base, args.to_base, args.precision
        )

        base_names = {2: "binary", 8: "octal", 10: "decimal", 16: "hexadecimal"}
        from_base_name = base_names[args.from_base]
        to_base_name = base_names[args.to_base]
        print(f"{args.number} ({from_base_name}) = {result} ({to_base_name})")

    except ConversionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
