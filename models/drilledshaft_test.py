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
        self.assertAlmostEqual(self.test_shaft.D, 20.0, places=3)

        self.assertAlmostEqual(
            self.test_shaft.concrete.beta1(), 0.75, places=2)

        self.assertAlmostEqual(self.test_shaft.steel.E, 29000000.0, places=0)

        self.assertAlmostEqual(self.test_shaft.concrete.ec, 0.003, places=3)

        self.assertAlmostEqual(self.test_shaft.c, 20.51791, places=4)

        self.assertAlmostEqual(self.test_shaft.alpha(), 2.13985, places=4)

        self.assertAlmostEqual(self.test_shaft.a, 15.38843, places=4)

        self.assertAlmostEqual(self.test_shaft.Ac(), 259.37708, places=2)

        self.assertAlmostEqual(self.test_shaft.ybar(), 1.53656, places=3)

        self.assertAlmostEqual(self.test_shaft.concrete.fc, 6000.0, places=-2)

        self.assertAlmostEqual(self.test_shaft.Cc()/1000.0, 1322.823, places=0)

        self.assertAlmostEqual(self.test_shaft.Mc()/1000.0, 2032.597, places=0)

        self.assertAlmostEqual(self.test_shaft._Pns() /
                               1000.0, 222.462, places=0)

        self.assertAlmostEqual(self.test_shaft._Pnc() /
                               1000.0, 1322.823, places=0)

        self.assertAlmostEqual(self.test_shaft.Pn()/1000.0, 1545.285, places=0)

        self.assertAlmostEqual(self.test_shaft.phiPn() /
                               1000.0, 1004.0, places=0)

        # Test locations of the bars
        self.assertAlmostEqual(self.test_shaft._dsi()[0], 10.000, places=3)
        self.assertAlmostEqual(self.test_shaft._dsi()[1], 3.452, places=3)
        self.assertAlmostEqual(self.test_shaft._dsi()[2], 3.452, places=3)
        self.assertAlmostEqual(self.test_shaft._dsi()[3], 10.000, places=3)
        self.assertAlmostEqual(self.test_shaft._dsi()[4], 16.548, places=3)
        self.assertAlmostEqual(self.test_shaft._dsi()[5], 16.548, places=3)

        # Test strains in bars
        self.assertAlmostEqual(self.test_shaft._esi()[0], 0.0015379, places=4)
        self.assertAlmostEqual(self.test_shaft._esi()[1], 0.0024953, places=4)
        self.assertAlmostEqual(self.test_shaft._esi()[2], 0.0024953, places=4)
        self.assertAlmostEqual(self.test_shaft._esi()[3], 0.0015379, places=4)
        self.assertAlmostEqual(self.test_shaft._esi()[4], 0.0005804, places=4)
        self.assertAlmostEqual(self.test_shaft._esi()[5], 0.0005804, places=4)

        # Test stresses in bars
        self.assertAlmostEqual(self.test_shaft._fsi()[
                               0]/1000.0, 44.598, places=3)
        self.assertAlmostEqual(self.test_shaft._fsi()[
                               1]/1000.0, 60.000, places=3)
        self.assertAlmostEqual(self.test_shaft._fsi()[
                               2]/1000.0, 60.000, places=3)
        self.assertAlmostEqual(self.test_shaft._fsi()[
                               3]/1000.0, 44.598, places=3)
        self.assertAlmostEqual(self.test_shaft._fsi()[
                               4]/1000.0, 16.833, places=3)
        self.assertAlmostEqual(self.test_shaft._fsi()[
                               5]/1000.0, 16.833, places=3)

        # Moment contribution from each bar
        self.assertAlmostEqual(self.test_shaft._Msi()[0]/1000.0, 0.0, places=1)
        self.assertAlmostEqual(self.test_shaft._Msi()[
                               1]/1000.0, 359.486, places=1)
        self.assertAlmostEqual(self.test_shaft._Msi()[
                               2]/1000.0, 359.486, places=1)
        self.assertAlmostEqual(self.test_shaft._Msi()[3]/1000.0, 0.0, places=1)
        self.assertAlmostEqual(self.test_shaft._Msi()[
                               4]/1000.0, -110.222, places=1)
        self.assertAlmostEqual(self.test_shaft._Msi()[
                               5]/1000.0, -110.222, places=1)

        self.assertAlmostEqual(self.test_shaft.Mn()/1000.0, 2531.125, places=1)


if __name__ == '__main__':
    unittest.main()
