#!/usr/bin/env python3
import unittest
from leglib.util import almost_equal
from .drilledshaft import DrilledShaft
from leglib.structural.acibars import bars
from leglib.structural.concrete import Concrete
from leglib.structural.acibars import a615_grade60
import math


class TestDrilledShaft(unittest.TestCase):

    def setUp(self):
        self.test_shaft = DrilledShaft(D=16.0)
        self.test_shaft.n = 8
        self.test_shaft.bar = bars["#9"]
        self.test_shaft.cover = 2.5 - self.test_shaft.bar.db/2.0
        self.test_shaft.c = 6.0

    # Test against results in article:
    # Tayem, A. and Najmi, A., "Design of Round Reinforced-Concrete Columns", Journal of Structural Engineering, September 1996

    def test_shaft_concrete(self):
        # assert(almost_equal(test_shaft.Ag, 201.061929829746767, places=4))

        # self.assertAlmostEqual(
        #     self.test_shaft._Ac(), 43.757, places=3)
        self.assertAlmostEqual(
            self.test_shaft.concrete.beta1(), 0.85, places=2)

        # assert(almost_equal(test_shaft._theta(), 0.253, places=3))
        # assert(almost_equal(test_shaft._gamma(), 0.371, places=3))
        # assert(almost_equal(test_shaft._z(), 1.459, places=3))
        # assert(almost_equal(test_shaft._Ac(), 43.743, places=3))
        # assert(almost_equal(test_shaft._Qc(), 190.867, places=3))
        # assert(almost_equal(test_shaft._cc(), 4.363, places=3))
        # assert(almost_equal(test_shaft._Ic(), 899.369, places=0))

class TestCircularColumn(unittest.TestCase):
    "Test case based upon 2008 CRSI Handbook manual example on p. 4-5"

    def setUp(self):
        self.test_shaft = DrilledShaft(D=20.0)
        self.test_shaft.n = 6
        self.test_shaft.bar = bars["#9"]
        self.test_shaft.cover = 1.5
        self.test_shaft.tiebar = bars["#3"]
        self.test_shaft.concrete.fc = 6000.0
        self.test_shaft.c = 20.51791

    def test_manual_calcs(self):
        self.assertAlmostEqual(self.test_shaft.concrete.beta1(), 0.75, places=2)

        self.assertAlmostEqual(self.test_shaft.steel.E, 29000000.0, places=0)

        self.assertAlmostEqual(self.test_shaft.concrete.ec, 0.003, places=3)

        self.assertAlmostEqual(self.test_shaft.a, 2.13985, places=4)


if __name__ == '__main__':
    unittest.main()

