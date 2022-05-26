'''
Unit tests for datediff module.
'''

import unittest

import datediff

class TestDateDiff(unittest.TestCase):
    '''
    Unit tests for datediff function.
    '''

    def test_same_day(self):
        '''
        Test two identical dates, i.e. no days in between.
        '''
        self.assertEqual(datediff.difference('2012-01-10', '2012-01-10'), 0)

    def test_consecutive_days(self):
        '''
        Test two consecutive dates, i.e. no days in between because endpoints
        are excluded.
        '''
        self.assertEqual(datediff.difference('2012-01-10', '2012-01-11'), 0)

    def test_dates_in_same_month(self):
        '''
        Test two dates that fall within the same calendar month.
        '''
        self.assertEqual(datediff.difference('2012-01-01', '2012-01-10'), 8)

    def test_dates_in_same_year(self):
        '''
        Test two dates that fall within the same year.
        '''
        self.assertEqual(datediff.difference('1801-06-13', '1801-11-11'), 150)

    def test_dates_in_different_years(self):
        '''
        Test two dates that are multiple years apart.
        '''
        self.assertEqual(datediff.difference('2017-12-14', '2021-12-01'), 1447)

    def test_reversed_arguments(self):
        '''
        Test that absolute value is returned when later date is provided first.
        '''
        self.assertEqual(datediff.difference('2021-12-01', '2017-12-14'), 1447)


class TestIsLeapYear(unittest.TestCase):
    '''
    Unit tests for is_leap_year function.
    '''

    def test_regular_non_leap_year(self):
        '''
        Test case for an obvious non-leap year (not divisible by 4).
        '''
        self.assertFalse(datediff.is_leap_year(2001))

    def test_regular_leap_year(self):
        '''
        Test case for an obvious leap year (divisible by 4, not a century).
        '''
        self.assertTrue(datediff.is_leap_year(2004))

    def test_non_leap_century(self):
        '''
        Test case for a century year that is not a leap year under the
        Gregorian calendar.
        '''
        self.assertFalse(datediff.is_leap_year(1900))

    def test_leap_century(self):
        '''
        Test case for a century year that is a leap year under the Gregorian
        calendar.
        '''
        self.assertTrue(datediff.is_leap_year(2000))


class TestParseDate(unittest.TestCase):
    '''
    Unit tests for parse_date function.
    '''

    def test_regular_date(self):
        '''
        Test a well-formatted date without any boundary conditions.
        '''
        self.assertEqual(datediff.parse_date('2022-05-26'),
                         datediff.Date(2022, 5, 26))

    def test_month_start_boundaries(self):
        '''
        Test that months start at day 1 and not day 0.
        '''
        for month in range(1, 13):
            month_str = str(month).zfill(2)
            self.assertEqual(datediff.parse_date(f'2020-{month_str}-01'),
                             datediff.Date(2020, month, 1))
            self.assertRaisesRegex(ValueError, r'.*day must be in range \[1-.*',
                    datediff.parse_date, f'2020-{month_str}-00')

    def test_30_day_month_end_boundaries(self):
        '''
        Test that all 30-day months include 30 and exclude 31.
        '''
        for month in [4, 6, 9, 11]:
            month_str = str(month).zfill(2)
            self.assertEqual(datediff.parse_date(f'2022-{month_str}-30'),
                             datediff.Date(2022, month, 30))
            self.assertRaisesRegex(ValueError,
                    r'.*day must be in range \[1-30\].*',
                    datediff.parse_date, f'2022-{month_str}-31')

    def test_31_day_month_end_boundaries(self):
        '''
        Test that all 31-day months include 31 and not 32.
        '''
        for month in [1, 3, 5, 7, 8, 10, 12]:
            month_str = str(month).zfill(2)
            self.assertEqual(datediff.parse_date(f'2022-{month_str}-31'),
                             datediff.Date(2022, month, 31))
            self.assertRaisesRegex(ValueError,
                    r'.*day must be in range \[1-31\].*',
                    datediff.parse_date, f'2022-{month_str}-32')

    def test_non_leap_february_boundary(self):
        '''
        Test upper boundary of a non-leap year February.
        '''
        self.assertEqual(datediff.parse_date('2021-02-28'),
                         datediff.Date(2021, 2, 28))
        self.assertRaisesRegex(ValueError,
                r'.*day must be in range \[1-28\].*',
                datediff.parse_date, '2021-02-29')

    def test_leap_february_boundary(self):
        '''
        Test upper boundary of a leap year February.
        '''
        self.assertEqual(datediff.parse_date('2020-02-29'),
                         datediff.Date(2020, 2, 29))
        self.assertRaisesRegex(ValueError,
                r'.*day must be in range \[1-29\].*',
                datediff.parse_date, '2020-02-30')

    def test_month_is_zero(self):
        '''
        Test date where month is zero (a potential 0-based error).
        '''
        self.assertRaisesRegex(ValueError,
                r'.*month must be in range \[1-12\].*',
                datediff.parse_date, '2020-00-01')

    def test_month_out_of_range(self):
        '''
        Test date with month greater than 12.
        '''
        self.assertRaisesRegex(ValueError,
                r'.*month must be in range \[1-12\].*',
                datediff.parse_date, '2020-13-01')

    def test_dd_mm_yyyy_ordering(self):
        '''
        Test date with Australian-style DD-MM-YYYY format.
        '''
        self.assertRaises(ValueError, datediff.parse_date, '01-01-2020')

    def test_yy_mm_dd_format(self):
        '''
        Test date with two-digit year format.
        '''
        self.assertRaises(ValueError, datediff.parse_date, '20-01-01')

    def test_year_before_0000(self):
        '''
        Test four character year that is less than 0.
        '''
        self.assertRaises(ValueError, datediff.parse_date, '-300-01-01')

    def test_year_beyond_9999(self):
        '''
        Test year with more than 4 digits.
        '''
        self.assertRaises(ValueError, datediff.parse_date, '20000-01-01')
