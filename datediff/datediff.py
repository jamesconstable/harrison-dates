# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring

from dataclasses import dataclass
from enum import IntEnum
import re
from typing import NoReturn, Optional

DATE_RE = re.compile(r'(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)',
                     re.ASCII)

class Month(IntEnum):
    JANUARY   = 1
    FEBRUARY  = 2
    MARCH     = 3
    APRIL     = 4
    MAY       = 5
    JUNE      = 6
    JULY      = 7
    AUGUST    = 8
    SEPTEMBER = 9
    OCTOBER   = 10
    NOVEMBER  = 11
    DECEMBER  = 12

@dataclass(frozen=True)
class Date:
    year: int
    month: int
    day: int

def difference(_date1: str, _date2: str) -> int:
    pass

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
    match = DATE_RE.fullmatch(string)
    if match is None:
        raise ValueError('Date string must be in the format "YYYY-MM-DD"')

    year = int(match.group('year'))
    month = int(match.group('month'))
    day = int(match.group('day'))

    if month < Month.JANUARY or month > Month.DECEMBER:
        raise ValueError('Invalid date: month must be in range '
            + f'[{Month.JANUARY.value}-{Month.DECEMBER.value}]')

    match month:
        case Month.FEBRUARY if is_leap_year(year):
            if not 1 <= day <= 29:
                raise_day_range_error(day, month, 29, year)
        case Month.FEBRUARY:
            if not 1 <= day <= 28:
                raise_day_range_error(day, month, 28, year)
        case Month.APRIL | Month.JUNE | Month.NOVEMBER | Month.SEPTEMBER:
            if not 1 <= day <= 30:
                raise_day_range_error(day, month, 30)
        case _:
            if not 1 <= day <= 31:
                raise_day_range_error(day, month, 31)

    return Date(year, month, day)

def raise_day_range_error(
        day: int,
        month: int,
        max_day: int,
        year: Optional[int] = None) -> NoReturn:
    raise ValueError(
        f'Invalid date: {Month(month).name} ({month}) has {max_day} days'
        + ('' if year is None else f' in {year}')
        + f'; day must be in range [1-{max_day}]')
