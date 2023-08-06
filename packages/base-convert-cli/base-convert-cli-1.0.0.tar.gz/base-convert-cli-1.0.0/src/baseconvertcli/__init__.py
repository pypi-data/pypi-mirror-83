#!/usr/bin/env python3

import sys
import re
import argparse

DIGITS = "0123456789ABCDEF"

class InvalidCliArgsError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class Base:
    def __init__(self, short_names, full_name, size):
        self.names = short_names + [full_name]
        self.full_name = full_name
        self.size = size
        self.reg = re.compile("^[{}]+$".format(DIGITS[:size]))

    def matches(self, s):
        return self.reg.match(s) is not None

    def parse(self, s):
        match = self.reg.match(s)
        if not match:
            raise RuntimeError("Failed to parse: {}".format(s))
        digits = match.group()
        return sum((self.size**i)*DIGITS.index(d)
                   for i, d in enumerate(reversed(digits)))

    def format(self, n):
        if n == 0:
            return "0"
        digits = []
        while n > 0:
            digits.append(DIGITS[n % self.size])
            n = n // self.size
        return "".join(reversed(digits))

    def __eq__(self, other):
        return isinstance(other, Base) and other.size == self.size

BASES = [
    Base(["d", "dec"], "decimal", 10),
    Base(["b", "bin"], "binary", 2),
    Base(["h", "hex"], "hexadecimal", 16),
    Base(["o", "oct"], "octal", 8),
]

COLOURS = {
    "red": "31"
}

def show(s, *fmt_args, bold=False, colour=None, newline=True, stream=sys.stdout):
    if stream.isatty() and (bold or colour):
        prefix = "\033["
        codes = []
        if bold:
            codes.append("1")
        if colour:
            codes.append(COLOURS[colour])
        prefix += ";".join(codes) + "m"
        s = prefix + s + "\033[0m"
    print(
        s.format(*fmt_args),
        end="\n" if newline else "",
        file=stream)

def show_newline():
    print()

def show_error(s, *fmt_args):
    show("ERROR! ", colour="red", newline=False, stream=sys.stderr)
    show(s, *fmt_args, stream=sys.stderr)

def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""Convert between number bases up to base-16.

The more specific the input, the more concise the output. If
you don't specify the input base or desired output base, then
the tool will output all possible (common) conversions. If you
specify the input (using the --from flag) and the output (using
the --to flag) then it'll just output a single conversion.

Special bases:
  n; names
  2; b, bin, binary
  8; o, oct, octal
 10; d, dec, decimal
 16; h, hex, hexadecimal

Examples:
  bs 0                     # many -> many
  bs --from 6 5            # base-6 -> many
  bs --from hexadecimal 5  # hex -> many
  bs --from hex --to dec F # hex -> dec
  bs -f h -t d F           # short version""")
    parser.add_argument("n", nargs="?", help="The number to convert. Can also be passed in ASCII/text format through standard input.")
    parser.add_argument("--from", "-f", required=False, dest="fr", help="The input base. Number or name.")
    parser.add_argument("--to", "-t", required=False, help="The output base. Number or name.")
    return parser

def parse_base(s):
    for base in BASES:
        if s in base.names:
            return base
    try:
        n = int(s)
    except ValueError:
        raise InvalidCliArgsError("Invalid base: {}".format(s))
    if n < 2:
        raise InvalidCliArgsError("Invalid base: {}".format(n))
    if n > len(DIGITS):
        raise InvalidCliArgsError("Only support up to base-16, but was given: {}".format(n))
    return Base([], "base-{}".format(n), n)

def do_conversion(args):
    if args.n:
        s = args.n
    else:
        s = sys.stdin.read()
    s = s.upper()
    if args.fr:
        base = parse_base(args.fr)
        if not base.matches(s):
            raise InvalidCliArgsError("Number doesn't match expected base: " + s)
        input_bases = [base]
    else:
        input_bases = [base for base in BASES if base.matches(s)]
        if not input_bases:
            raise InvalidCliArgsError("Unsupported base, must be <=16.")
    if args.to:
        output_bases = [parse_base(args.to)]
    else:
        output_bases = BASES
    if len(input_bases) == 1 and len(output_bases) == 1:
        n = input_bases[0].parse(s)
        show(output_bases[0].format(n))
    else:
        for i, base in enumerate(input_bases):
            n = base.parse(s)
            if all(obase == base for obase in output_bases):
                # Don't print anything if there's only a pointless
                # conversion (from a base to itself).
                continue

            show("[from {}]", base.full_name, bold=True)
            max_name_length = max(len(base.full_name) for base in output_bases)
            for output_base in output_bases:
                if output_base != base:
                    show(
                        "  {:<" + str(max_name_length+1) + "}{}",
                        output_base.full_name,
                        output_base.format(n))
            if i != len(input_bases) - 1:
                show_newline()

def main():
    parser = get_parser()
    args = parser.parse_args()
    try:
        do_conversion(args)
    except InvalidCliArgsError as e:
        show_error(e.message)
        sys.exit(1)

if __name__ == "__main__":
    main()
