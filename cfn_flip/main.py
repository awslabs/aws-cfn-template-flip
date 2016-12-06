#!/usr/bin/env python

from . import flip
import sys

def main():
    """
    Figure out the input and output stream
    Then figure out the input format and set the opposing output format
    """

    ins = open(sys.argv[1], "r") if len(sys.argv) > 1 else sys.stdin
    outs = open(sys.argv[2], "w") if len(sys.argv) > 2 else sys.stdout

    template = ins.read()

    try:
        outs.write(flip(template))
    except Exception as e:
        sys.stderr.write("{}\n".format(str(e)))
        sys.exit(1)
