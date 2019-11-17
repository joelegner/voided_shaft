#!/usr/bin/env python3
import math

from leglib.structural.acibars import a615_grade60, bars
from leglib.structural.concrete import Concrete
from models.drilledshaft import DrilledShaft
from models.voidedshaft import VoidedShaft


class CompositeVoidedShaft(VoidedShaft):

    def __init__(self, D=96.0, Di=48.0, tc=0.625):
        "D = outer diameter in inches; Di = inner diameter in inches"
        VoidedShaft.__init__(self, D, Di)
        self.tc = tc
        self._build_casing()

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = value
        self._build_casing()

    def __str__(self):
        return "Composite %d inch diameter drilled shaft with %d inch diameter void with %.3f-inch thick casing" % (self.D, self.Di, self.tc)

    def _build_casing(self):
        "Builds the voided shaft object's casing object"
        print(type(self))
        self.casing = VoidedShaft(D=self.Di, Di=self.Di - 2.0*self.tc)
        self.casing.c = self.c - (self.D - self.Di)/2.0/self.concrete.beta1()
