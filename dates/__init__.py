'''
This module implements the harrison.ai tech task, "A delta of days":
<https://github.com/harrison-ai/hai-tech-tasks/blob/develop/dates.md>.

It can be run directly from the command line with the usage:
`python -m dates <date1> <date2>`

The only accepted date format is YYYY-MM-DD.
'''

from ._dates import Date, days_between, is_leap_year, parse_date

__all__ = ['Date', 'days_between', 'is_leap_year', 'parse_date']
