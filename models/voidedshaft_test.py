#!/usr/bin/env python3
import unittest
from leglib.util import almost_equal
from .voidedshaft import VoidedShaft
from leglib.structural.acibars import bars
from leglib.structural.concrete import Concrete
from leglib.structural.acibars import a615_grade60
import math


class TestVoidedShaft(unittest.TestCase):

    def setUp(self):
        self.test_shaft = VoidedShaft(D=16.0, Di=3.0)
        self.test_shaft.n = 8
        self.test_shaft.bar = bars["#9"]
        self.test_shaft.cover = 2.5 - self.test_shaft.bar.db/2.0
        self.test_shaft.c = 6.0

    # Test against results in article:
    # Tayem, A. and Najmi, A., "Design of Round Reinforced-Concrete Columns", Journal of Structural Engineering, September 1996

    def test_shaft_concrete(self):
        self.assertAlmostEqual(
            self.test_shaft.concrete.beta1(), 0.85, places=2)


class TestVoidedShaft(unittest.TestCase):
    "Test case based upon 2008 CRSI Handbook manual example on p. 4-5"

    def setUp(self):
        self.test_shaft = VoidedShaft(D=20.0, Di=8.0)
        self.test_shaft.n = 6
        self.test_shaft.bar = bars["#9"]
        self.test_shaft.cover = 1.5
        self.test_shaft.tiebar = bars["#3"]
        self.test_shaft.concrete.fc = 6000.0
        self.test_shaft.c = 10.0/0.75

    def test_manual_calcs(self):
        self.assertAlmostEqual(self.test_shaft.D, 20.0, places=3)

        self.assertAlmostEqual(
            self.test_shaft.concrete.beta1(), 0.75, places=2)

        self.assertAlmostEqual(self.test_shaft.steel.E, 29000000.0, places=0)

        self.assertAlmostEqual(self.test_shaft.concrete.ec, 0.003, places=3)

        self.assertAlmostEqual(self.test_shaft.c, 10.0/0.75, places=4)

        # self.assertAlmostEqual(self.test_shaft.alpha(), 2.13985, places=4)

        self.assertAlmostEqual(self.test_shaft.a, 10.0, places=4)

        R = self.test_shaft.D/2.0
        Ri = self.test_shaft.Di/2.0
        self.assertAlmostEqual(self.test_shaft.Ac(),
                               math.pi*(R**2 - Ri**2)/2.0, places=4)

        b = (R + Ri)/2.0
        t = R + Ri
        # self.assertAlmostEqual(self.test_shaft.ybar(),
        #                        2.0*b/math.pi*(1.0 + ((t/b)**2)/12.0), places=3)

#         self.assertAlmostEqual(self.test_shaft.concrete.fc, 6000.0, places=-2)

#         self.assertAlmostEqual(self.test_shaft.Cc()/1000.0, 1322.823, places=0)

#         self.assertAlmostEqual(self.test_shaft.Mc()/1000.0, 2032.597, places=0)

#         self.assertAlmostEqual(self.test_shaft._Pns() /
#                                1000.0, 222.462, places=0)

#         self.assertAlmostEqual(self.test_shaft._Pnc() /
#                                1000.0, 1322.823, places=0)

#         self.assertAlmostEqual(self.test_shaft.Pn()/1000.0, 1545.285, places=0)

#         self.assertAlmostEqual(self.test_shaft.phiPn() /
#                                1000.0, 1004.0, places=0)

#         # Test locations of the bars
#         self.assertAlmostEqual(self.test_shaft._dsi()[0], 10.000, places=3)
#         self.assertAlmostEqual(self.test_shaft._dsi()[1], 3.452, places=3)
#         self.assertAlmostEqual(self.test_shaft._dsi()[2], 3.452, places=3)
#         self.assertAlmostEqual(self.test_shaft._dsi()[3], 10.000, places=3)
#         self.assertAlmostEqual(self.test_shaft._dsi()[4], 16.548, places=3)
#         self.assertAlmostEqual(self.test_shaft._dsi()[5], 16.548, places=3)

#         # Test strains in bars
#         self.assertAlmostEqual(self.test_shaft._esi()[0], 0.0015379, places=4)
#         self.assertAlmostEqual(self.test_shaft._esi()[1], 0.0024953, places=4)
#         self.assertAlmostEqual(self.test_shaft._esi()[2], 0.0024953, places=4)
#         self.assertAlmostEqual(self.test_shaft._esi()[3], 0.0015379, places=4)
#         self.assertAlmostEqual(self.test_shaft._esi()[4], 0.0005804, places=4)
#         self.assertAlmostEqual(self.test_shaft._esi()[5], 0.0005804, places=4)

#         # Test stresses in bars
#         self.assertAlmostEqual(self.test_shaft._fsi()[
#                                0]/1000.0, 44.598, places=3)
#         self.assertAlmostEqual(self.test_shaft._fsi()[
#                                1]/1000.0, 60.000, places=3)
#         self.assertAlmostEqual(self.test_shaft._fsi()[
#                                2]/1000.0, 60.000, places=3)
#         self.assertAlmostEqual(self.test_shaft._fsi()[
#                                3]/1000.0, 44.598, places=3)
#         self.assertAlmostEqual(self.test_shaft._fsi()[
#                                4]/1000.0, 16.833, places=3)
#         self.assertAlmostEqual(self.test_shaft._fsi()[
#                                5]/1000.0, 16.833, places=3)

#         # Moment contribution from each bar
#         self.assertAlmostEqual(self.test_shaft._Msi()[0]/1000.0, 0.0, places=1)
#         self.assertAlmostEqual(self.test_shaft._Msi()[
#                                1]/1000.0, 359.486, places=1)
#         self.assertAlmostEqual(self.test_shaft._Msi()[
#                                2]/1000.0, 359.486, places=1)
#         self.assertAlmostEqual(self.test_shaft._Msi()[3]/1000.0, 0.0, places=1)
#         self.assertAlmostEqual(self.test_shaft._Msi()[
#                                4]/1000.0, -110.222, places=1)
#         self.assertAlmostEqual(self.test_shaft._Msi()[
#                                5]/1000.0, -110.222, places=1)

#         self.assertAlmostEqual(self.test_shaft.Mn()/1000.0, 2531.125, places=1)

#     def test_et_005_strain(self):
#         self.test_shaft.c = 6.20551    # Given in CRSI
#         self.assertAlmostEqual(self.test_shaft.D, 20.0, places=3)
#         self.assertAlmostEqual(self.test_shaft.phi(), 0.90, places=2)

#         self.assertAlmostEqual(
#             self.test_shaft.concrete.beta1(), 0.75, places=2)

#         self.assertAlmostEqual(self.test_shaft.steel.E, 29000000.0, places=0)

#         self.assertAlmostEqual(self.test_shaft.concrete.ec, 0.003, places=3)

#         self.assertAlmostEqual(self.test_shaft.c, 6.20551, places=4)

#         self.assertAlmostEqual(self.test_shaft.a, 4.65413, places=4)

#         self.assertAlmostEqual(self.test_shaft.Ac(), 55.49907, places=2)

#         self.assertAlmostEqual(self.test_shaft.ybar(), 7.25050, places=3)

#         self.assertAlmostEqual(self.test_shaft.concrete.fc, 6000.0, places=-2)

#         self.assertAlmostEqual(self.test_shaft.Cc()/1000.0, 283.045, places=0)

#         self.assertAlmostEqual(self.test_shaft.Mc()/1000.0, 2052.220, places=0)

#         self.assertAlmostEqual(self.test_shaft._Pns() /
#                                1000.0, -159.388, places=0)

#         self.assertAlmostEqual(self.test_shaft._Pnc() /
#                                1000.0, 283.045, places=0)

#         self.assertAlmostEqual(self.test_shaft.Pn()/1000.0, 123.657, places=0)
#         self.assertAlmostEqual(self.test_shaft.phiPn()/1000.0, 111.0, places=0)


# if __name__ == '__main__':
#     unittest.main()
