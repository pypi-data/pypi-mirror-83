# Copyright 2019-2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""CLI commands"""

import argparse
import sys
from pathlib import Path

import zoomrlib

PROGNAME = "zoomrlib"


def _create_parser():
    """Return parser for this script."""
    parser = argparse.ArgumentParser(
        prog=PROGNAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
Read content of a ZoomR project and print it to stdout as json format.
        """,
    )
    parser.add_argument(
        "zdtfile",
        metavar="ZDTFILE",
        help="ZDT file that that need to be read.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + zoomrlib.__version__,
    )
    return parser


def main():
    """Program starts here."""
    args = _create_parser().parse_args()
    zdtpath = Path(args.zdtfile)
    if not zdtpath.exists():
        print("Error: Can not open file %s" % str(zdtpath), file=sys.stderr)
        sys.exit(1)
    with zoomrlib.open(zdtpath) as file:
        project = zoomrlib.load(file)
    print(project.tojson())
    sys.exit(0)
