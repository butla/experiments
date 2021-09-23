import unittest
from datetime import datetime
from unittest import TestCase

from task_time_calc import calculate_entire_time, TIME_ZERO


class TestCalculations(TestCase):
    def test_absolute_time(self):
        self.assertEqual(
            str(datetime.strptime('11 16', '%H %M') - TIME_ZERO),
            calculate_entire_time('1:13, 0:03, 10:00'))

    def test_time_ranges(self):
        self.assertEqual(
            str(datetime.strptime('6 10', '%H %M') - TIME_ZERO),
            calculate_entire_time('1:13 - 3:23, 14:00-18:00'))

    def test_time_ranges_accross_days(self):
        self.assertEqual(
            str(datetime.strptime('4 00', '%H %M') - TIME_ZERO),
            calculate_entire_time('23:00 - 3:00'))


if __name__ == '__main__':
    unittest.main()
