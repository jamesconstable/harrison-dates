import unittest

from dates import is_leap_year

class TestIsLeapYear(unittest.TestCase):
    '''
    Unit tests for is_leap_year function.
    '''

    def test_regular_non_leap_year(self):
        '''
        Test case for an obvious non-leap year (not divisible by 4).
        '''
        self.assertFalse(is_leap_year(2001))

    def test_regular_leap_year(self):
        '''
        Test case for an obvious leap year (divisible by 4, not a century).
        '''
        self.assertTrue(is_leap_year(2004))

    def test_non_leap_century(self):
        '''
        Test case for a century year that is not a leap year under the
        Gregorian calendar.
        '''
        self.assertFalse(is_leap_year(1900))

    def test_leap_century(self):
        '''
        Test case for a century year that is a leap year under the Gregorian
        calendar.
        '''
        self.assertTrue(is_leap_year(2000))
