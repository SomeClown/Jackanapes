#!/usr/local/bin/python3


import arg_proc
import pq_args

__author__ = 'SomeClown'

"""
Command Line Twitter Client
The goal of this project is to implement all functionality from the Twitter API via a traditional Unix interface.
Command line Twitter (and stuff) client - For questions contact @SomeClown
"""


def main() -> object:
    my_command_args = pq_args.argumentsParsing()
    arg_proc.arglebarg(my_command_args)
    return None


if __name__ == "__main__":
    main()
else:
    pass
