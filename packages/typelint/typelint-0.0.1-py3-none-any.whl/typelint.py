#!/usr/bin/env python

# https://docs.python.org/3/library/argparse.html
import argparse
# https://docs.python.org/3/library/ast.html
import ast

import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description="List type hints")
    parser.add_argument("files", type=str, nargs="+")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    total_lints = 0

    for arg in args.files:
        with open(arg) as f:
            hints = typelint(f)
            total_lints += len(hints)
            if not args.quiet:
                for hint in hints:
                    print(hint)

    return min(99, total_lints)


def typelint(fildes):
    """
    Given an open file object, return a sequence (list, really)
    of all the typehints discovered.
    Ideally there are none, in which case the empty list is
    returned.
    """

    source = fildes.read()

    tree = ast.parse(source)

    type_annotations = []

    for node in ast.walk(tree):
        returns = getattr(node, "returns", None)
        if returns:
            type_annotations.append(returns)

    return type_annotations


if __name__ == "__main__":
    sys.exit(main())
