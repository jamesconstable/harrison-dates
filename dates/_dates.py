'''
This private submodule contains all of the date-related functionality,
including representation, parsing, and the `days_between` calculation described
in the problem spec.
'''

from dataclasses import dataclass
from enum import IntEnum
import re
from typing import NoReturn

# Regex representing the allowed 'YYYY-MM-DD' date format.
DATE_RE = re.compile(r'(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)',
                     re.ASCII)

# Number of days in one full leap cycle (400 years). Every fourth year is a
# leap year (of 400 years, that's 100), except for centuries (that's 4) but not
# those also divisible by 400 (just the first). So the number of leap years in
# one cycle is 100 - 4 + 1 = 97, and the rest are non-leaps, 400 - 97 = 303.
DAYS_IN_LEAP_CYCLE = 97 * 366 + 303 * 365


class Month(IntEnum):
    '''
    Represents the months of the year. Integer values are 1-based.
    '''
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12

    def days_in_year(self, year: int) -> int:
        '''
        Returns the number of days in this month in the given year.
        '''
        match self:
            case Month.FEBRUARY if is_leap_year(year):
                return 29
            case Month.FEBRUARY:
                return 28
            case Month.APRIL | Month.JUNE | Month.NOVEMBER | Month.SEPTEMBER:
                return 30
        return 31


@dataclass(frozen=True)
class Date:
    '''
    Represents a date in the proleptic Gregorian calendar.
    '''
    year: int
    month: Month
    day: int

    def days_since_epoch(self) -> int:
        '''
        Returns the number of days that have elapsed since 1BC-01-01 in the
        proleptic Gregorian calendar (`Date(0, 1, 1)`), not including `date`.
        '''
        # Rather than counting up from 1BC each time, start at the beginning of
        # the 400-year leap cycle that contains `date`.
        total = (self.year // 400) * DAYS_IN_LEAP_CYCLE
        for year in range(self.year % 400):
            total += 366 if is_leap_year(year) else 365
        for month in range(Month.JANUARY, self.month):
            total += Month(month).days_in_year(self.year)
        return total + self.day - 1


def days_between(date1: Date | str, date2: Date | str) -> int:
    '''
    Returns the number of days between date1 and date2, not including the start
    and end dates. Result is always a positive integer (the absolute number of
    intervening days); the chronological order of the arguments is not
    important. Raises a `ValueError` if either argument cannot be parsed into
    a valid `Date`.
    '''
    if isinstance(date1, str):
        date1 = parse_date(date1)
    if isinstance(date2, str):
        date2 = parse_date(date2)
    difference = abs(date1.days_since_epoch() - date2.days_since_epoch())
    return max(0, difference - 1)


def is_leap_year(year: int) -> bool:
    '''
    Returns True if the given year is a leap year according to the proleptic
    Gregorian calendar (i.e. extrapolating the modern rules indefinitely
    forward and backward in time) and False otherwise.
    '''
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False


def parse_date(string: str) -> Date:
    '''
    Attempts to parse the given string into a `Date`. Raises a `ValueError` if
    the string is not in the format "YYYY-MM-DD" or does not represent a valid
    date.
    '''
    match = DATE_RE.fullmatch(string)
    if match is None:
        raise ValueError(
                f'Invalid date "{string}": must be in the format "YYYY-MM-DD"')

    year = int(match.group('year'))
    month = int(match.group('month'))
    day = int(match.group('day'))

    if not Month.JANUARY <= month <= Month.DECEMBER:
        raise ValueError(f'Invalid date "{string}": month must be in range ' +
                         f'[{Month.JANUARY.value}-{Month.DECEMBER.value}]')

    month = Month(month)
    if not 1 <= day <= month.days_in_year(year):
        raise_day_range_error(string, month, year)

    return Date(year, month, day)


def raise_day_range_error(string: str, month: Month, year: int) -> NoReturn:
    '''
    Helper function for raising descriptive errors when a day is outside the
    normal bounds for a month.
    '''
    max_day = month.days_in_year(year)
    raise ValueError(
        f'Invalid date "{string}": {Month(month).name} has {max_day} days'
        + (f' in {year}' if month is Month.FEBRUARY else '')
        + f'; day must be in range [1-{max_day}]')
