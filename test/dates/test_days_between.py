'''
This submodule contains the unit tests for the `dates.days_between` function.
'''

import unittest

from dates import days_between


class TestDaysBetween(unittest.TestCase):
    '''
    Unit tests for days_between function.
    '''

    def test_same_day(self):
        '''
        Test two identical dates, i.e. no days in between.
        '''
        self.assertEqual(days_between('2012-01-10', '2012-01-10'), 0)

    def test_consecutive_days(self):
        '''
        Test two consecutive dates, i.e. no days in between because endpoints
        are excluded.
        '''
        self.assertEqual(days_between('2012-01-10', '2012-01-11'), 0)

    def test_days_one_apart(self):
        '''
        Test two dates which have one intervening day.
        '''
        self.assertEqual(days_between('2012-01-10', '2012-01-12'), 1)

    def test_dates_in_same_month(self):
        '''
        Test two dates that fall within the same calendar month.
        '''
        self.assertEqual(days_between('2012-01-01', '2012-01-10'), 8)

    def test_dates_in_same_year(self):
        '''
        Test two dates that fall within the same year.
        '''
        self.assertEqual(days_between('1801-06-13', '1801-11-11'), 150)

    def test_dates_in_different_years(self):
        '''
        Test two dates that are multiple years apart.
        '''
        self.assertEqual(days_between('2017-12-14', '2021-12-01'), 1447)

    def test_reversed_arguments(self):
        '''
        Test that absolute value is returned when later date is provided first.
        '''
        self.assertEqual(days_between('2021-12-01', '2017-12-14'), 1447)

    def test_range_from_zero(self):
        '''
        Test that ranges starting at the earliest representable date
        (1 BC = 0000) are handled correctly.
        '''
        self.assertEqual(days_between('0000-01-01', '0001-03-01'), 424)

    def test_historical_calendar_changes(self):
        '''
        Test a range that encompasses the Julian-to-Gregorian changeover
        (result should assume no change and use the Gregorian calendar
        throughout).
        '''
        self.assertEqual(days_between('1000-01-01', '2000-01-01'), 365241)

    def test_invalid_date(self):
        '''
        Test that date parsing errors are propagated correctly.
        '''
        self.assertRaises(ValueError, days_between, '20-01-01', '2000-05-01')
