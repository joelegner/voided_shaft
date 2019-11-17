#!/usr/bin/env python3
import unittest
from leglib.util import almost_equal
from models.comp_voidedshaft import CompositeVoidedShaft
from leglib.structural.acibars import bars
from leglib.structural.concrete import Concrete
from leglib.structural.acibars import a615_grade60
import math


class TestCompositeVoidedShaftSuperclass(unittest.TestCase):

    def setUp(self):
        self.test_shaft = CompositeVoidedShaft(D=16.0, Di=3.0, tc=0.0)
        self.test_shaft.n = 8
        self.test_shaft.bar = bars["#9"]
        self.test_shaft.cover = 2.5 - self.test_shaft.bar.db/2.0
        self.test_shaft.D = 20.0
        self.test_shaft.Di = 12.0
        # Set c so as to result in a = 9 inches by dividing by beta1
        self.test_shaft.c = 9.0/self.test_shaft.concrete.beta1()

    def test_voided_shaft_shape_props(self):
        # Solid shape without void removed
        self.assertAlmostEqual(self.test_shaft.theta_0(),
                               1.4706289056333368, 4)
        self.assertAlmostEqual(self.test_shaft.Ac_0(), 137.11301619226748, 4)
        self.assertAlmostEqual(self.test_shaft.ybar_0(), 4.789419172061094, 4)

        # Void area
        self.assertAlmostEqual(self.test_shaft.theta_i(),
                               1.4033482475752073, 4)
        self.assertAlmostEqual(self.test_shaft.Ac_i(), 44.604457129607844, 4)
        self.assertAlmostEqual(self.test_shaft.ybar_i(), 3.094799723815658, 4)

        # Net shape = solid with void area deducted
        self.assertAlmostEqual(self.test_shaft.Ac(), 92.50855906265963, 4)
        self.assertAlmostEqual(self.test_shaft.ybar(), 5.606506599388385, 4)

class TestCompositeVoidedShaftSuperclass(unittest.TestCase):

    def setUp(self):
        self.test_shaft = CompositeVoidedShaft(D=108.0, Di=48.0, tc=0.625)
        self.test_shaft.n = 36
        self.test_shaft.steel.fy = 60000.0
        self.test_shaft.concrete.fc = 4000.0
        self.test_shaft.cover = 6.0
        self.test_shaft.set_bar_size("#9")
        self.test_shaft.set_tiebar_size("#5")

        # Set c so as to result in a = 54 inches by dividing by beta1
        self.test_shaft.c = 54.0/self.test_shaft.concrete.beta1()

    def test_liner_shape_props(self):
        self.assertAlmostEqual(self.test_shaft.casing.Ag, 93.021, places=3)
        self.assertAlmostEqual(self.test_shaft.casing.a, 24.0, places=3)
        self.assertAlmostEqual(self.test_shaft.casing.Ac(), 46.510, places=3)



if __name__ == '__main__':
    unittest.main()
