"""Experimental syntax notation for fraction literal

n F -> Fraction(n) where n is an integer
"""

import token_utils  # Need to be installed separately

__version__ = "0.0.1"

import_statement = "from fractions import Fraction"


def transform_source(source):
    tokens = token_utils.tokenize(source)
    if len(tokens) < 2:
        return source
    for first, second in zip(tokens, tokens[1:]):
        if first.is_integer() and second == "F":
            first.string = f"Fraction({first.string})"
            second.string = ""

    return token_utils.untokenize(tokens)


if __name__ == "__main__":
    original = "a = 3F / 25F"
    transformed = "a = Fraction(3) / Fraction(25)"
    assert transform_source(original) == transformed
    print("Looks good")
