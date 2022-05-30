# pylint: disable=missing-module-docstring

import sys

import dates

USAGE_MSG = 'Usage: python -m dates <date1> <date2>\nDate format: YYYY-MM-DD'

match sys.argv[1:]:
    case [date1, date2]:
        try:
            print(dates.days_between(date1, date2))
        except ValueError as err:
            print(err, file=sys.stderr)
            sys.exit(2)
    case ['-h'] | ['--help']:
        print(USAGE_MSG)
    case _:
        print(sys.argv)
        print(USAGE_MSG, file=sys.stderr)
        sys.exit(1)
