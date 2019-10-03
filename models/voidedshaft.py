#!/usr/bin/env python3
from models.drilledshaft import DrilledShaft
from leglib.structural.acibars import bars
from leglib.structural.concrete import Concrete
from leglib.structural.acibars import a615_grade60
import math


class VoidedShaft(DrilledShaft):

    def __init__(self, D=96.0, Di=48.0):
        """
        D = outer diameter in inches
        Di = inner diameter in inches
        """
        self.D = D
        self.Di = Di
        self.n = 24
        self.bar = bars["#10"]
        self.tiebar = bars["#4"]
        self.cover = 6.0
        self.concrete = Concrete(4000.0)
        self.steel = a615_grade60
        self.c = 1.0

    def __str__(self):
        return "%d inch diameter drilled shaft with %d inch diameter void" % (self.D, self.Di)

    def Ac(self):
        h = self.Di
        alpha = self.alpha()
        return super(VoidedShaft, self).Ac() - self._Ac_inner()

    def _Ac_inner(self):
        R = self.D/2.0
        Ri = self.Di/2.0
        h = self.a - R + Ri
        if h > 0:
            r = Ri - h
            theta = 2.0*math.acos(r/Ri)
            return 0.5*Ri*Ri*(theta - math.sin(theta))
        else:
            return 0

    def _ybar_inner(self):
        R = self.D/2.0
        Ri = self.Di/2.0
        h = self.a - R + Ri
        r = Ri - h
        theta = 2.0*math.acos(r/Ri)
        return 4*Ri*math.sin(0.5*theta)**3/(3.0*(theta - math.sin(theta)))

    def ybar(self):
        "Returns distance of concrete centroid from column centroid at y=c"
        A1 = super(VoidedShaft, self).Ac()
        y1 = super(VoidedShaft, self).ybar()
        A2 = self._Ac_inner()
        y2 = self._ybar_inner()
        return (A1*y1 - A2*y2)/(A2 + A2)

    def Ag(self):
        "Returns gross area in square inches"
        return super(VoidedShaft, self).Ag() - math.pi*self.Di**2/4.0
