import unittest
import datediff

class TestDatediff(unittest.TestCase):
    '''
    Unit tests for datediff module.
    '''

    def testSameDay(self):
        self.assertEqual(datediff.difference('2012-01-10', '2012-01-10'), 0)

    def testConsecutiveDays(self):
        self.assertEqual(datediff.difference('2012-01-10', '2012-01-11'), 0)

    def testDaysInSameMonth(self):
        self.assertEqual(datediff.difference('2012-01-01', '2012-01-10'), 8)

    def testDaysInSameYear(self):
        self.assertEqual(datediff.difference('1801-06-13', '1801-11-11'), 150)

    def testEarlierSecondDate(self):
        self.assertEqual(datediff.difference('2021-12-01', '2017-12-14'), 1447)
