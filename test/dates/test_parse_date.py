import unittest

from dates import Date, parse_date

class TestParseDate(unittest.TestCase):
    '''
    Unit tests for parse_date function.
    '''

    def test_regular_date(self):
        '''
        Test a well-formatted date without any boundary conditions.
        '''
        self.assertEqual(parse_date('2022-05-26'),
                         Date(2022, 5, 26))

    def test_month_start_boundaries(self):
        '''
        Test that months start at day 1 and not day 0.
        '''
        for month in range(1, 13):
            month_str = str(month).zfill(2)
            self.assertEqual(parse_date(f'2020-{month_str}-01'),
                             Date(2020, month, 1))
            self.assertRaisesRegex(ValueError, r'.*day must be in range \[1-.*',
                    parse_date, f'2020-{month_str}-00')

    def test_30_day_month_end_boundaries(self):
        '''
        Test that all 30-day months include 30 and exclude 31.
        '''
        for month in [4, 6, 9, 11]:
            month_str = str(month).zfill(2)
            self.assertEqual(parse_date(f'2022-{month_str}-30'),
                             Date(2022, month, 30))
            self.assertRaisesRegex(ValueError,
                    r'.*day must be in range \[1-30\].*',
                    parse_date, f'2022-{month_str}-31')

    def test_31_day_month_end_boundaries(self):
        '''
        Test that all 31-day months include 31 and not 32.
        '''
        for month in [1, 3, 5, 7, 8, 10, 12]:
            month_str = str(month).zfill(2)
            self.assertEqual(parse_date(f'2022-{month_str}-31'),
                             Date(2022, month, 31))
            self.assertRaisesRegex(ValueError,
                    r'.*day must be in range \[1-31\].*',
                    parse_date, f'2022-{month_str}-32')

    def test_non_leap_february_boundary(self):
        '''
        Test upper boundary of a non-leap year February.
        '''
        self.assertEqual(parse_date('2021-02-28'),
                         Date(2021, 2, 28))
        self.assertRaisesRegex(ValueError,
                r'.*day must be in range \[1-28\].*',
                parse_date, '2021-02-29')

    def test_leap_february_boundary(self):
        '''
        Test upper boundary of a leap year February.
        '''
        self.assertEqual(parse_date('2020-02-29'),
                         Date(2020, 2, 29))
        self.assertRaisesRegex(ValueError,
                r'.*day must be in range \[1-29\].*',
                parse_date, '2020-02-30')

    def test_month_is_zero(self):
        '''
        Test date where month is zero (a potential 0-based error).
        '''
        self.assertRaisesRegex(ValueError,
                r'month.*must be in range \[1-12\].*',
                parse_date, '2020-00-01')

    def test_month_out_of_range(self):
        '''
        Test date with month greater than 12.
        '''
        self.assertRaisesRegex(ValueError,
                r'month.*must be in range \[1-12\].*',
                parse_date, '2020-13-01')

    def test_dd_mm_yyyy_ordering(self):
        '''
        Test date with Australian-style DD-MM-YYYY format.
        '''
        self.assertRaises(ValueError, parse_date, '01-01-2020')

    def test_yy_mm_dd_format(self):
        '''
        Test date with two-digit year format.
        '''
        self.assertRaises(ValueError, parse_date, '20-01-01')

    def test_year_before_0000(self):
        '''
        Test four character year that is less than 0.
        '''
        self.assertRaises(ValueError, parse_date, '-300-01-01')

    def test_year_beyond_9999(self):
        '''
        Test year with more than 4 digits.
        '''
        self.assertRaises(ValueError, parse_date, '20000-01-01')
