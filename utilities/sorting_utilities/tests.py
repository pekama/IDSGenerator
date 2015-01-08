__author__ = 'eyal'

from unittest import TestCase
from utilities.sorting_utilities.sorting_utilities import NaturalSortingStrategy


class NaturalSortingStrategyTests(TestCase):

    def test_sort(self):
        l = ['A2-2','A3-1','A2-11']

        sorter = NaturalSortingStrategy()

        self.assertEqual(sorter.sort(l), ['A2-2', 'A2-11', 'A3-1'])