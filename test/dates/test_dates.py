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