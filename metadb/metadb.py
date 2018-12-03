#!/usr/bin/env python3
import os,argparse
from sql import *

def parse_cmd_args():
    ''' command line argument parser based on argparse module '''
    desc = '\n'.join(["Database for tracking file metadata information",
                      "Authors: Sergiy Kolodyazhnyy, Liu Tian, Jericha Bradley",
                      "Written for CS 3810, Fall 2018"
           ])
    argp = argparse.ArgumentParser(description=desc,formatter_class=argparse.RawTextHelpFormatter)

    argp.add_argument(
        "-l","--load",
        action='store_true',
        help=': Traverse XDG directories and imports metadata for each file'
    )

    argp.add_argument(
        "-v","--vacuum",
        action='store_true'
    )

    argp.add_argument(
        "-f","--file",
        type=str,
        help=': Prints full information for a particular filename'
    )

    return argp.parse_args()


def main():
    ''' Program entry point '''
    args = parse_cmd_args()

    if args.load:
        load_db()
        sys.exit(0)

    if args.vacuum:
       vacuum()
       sys.exit(0)

    if args.file:
       find_file(args.file)


if __name__ == '__main__':
    main()
