'''
Command line runner for the `days_between` functionality. Accepts two dates in
the format "YYYY-MM-DD" and outputs the number of days between them to stdout.
All calculations assume the proleptic Gregorian calendar (i.e. extrapolating
the modern rules for leap years indefinitely both forwards and backwards), and
the year 1 BC may be expressed as 0000.
'''

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
        print(USAGE_MSG, file=sys.stderr)
        sys.exit(1)
