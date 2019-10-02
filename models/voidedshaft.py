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
        return super(VoidedShaft, self).Ac() - h**2*(2.0*alpha - math.sin(2*alpha))/8.0

    def ybar(self):
        "Returns distance of concrete centroid from column centroid at y=c"
        h = self.Di
        alpha = self.alpha()
        return super(VoidedShaft, self).ybar() - (2.0*h**3)*math.sin(alpha)**3/(24.0*self.Ac())

    def Ag(self):
        "Returns gross area in square inches"
        return super(VoidedShaft, self).Ag() - math.pi*self.Di**2/4.0
