#!/usr/local/bin/python3

import arg_proc
import pq_args


def main() -> object:
    my_command_args = pq_args.argumentsParsing()
    arg_proc.arglebarg(my_command_args)
    return None


if __name__ == "__main__":
    main()

else:
    print('Loaded as module')
