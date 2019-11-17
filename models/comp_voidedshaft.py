#!/usr/bin/env python3
import math

from leglib.structural.acibars import a615_grade60, bars
from leglib.structural.concrete import Concrete
from models.drilledshaft import DrilledShaft
from models.voidedshaft import VoidedShaft


class CompositeVoidedShaft(VoidedShaft):

    def __init__(self, D=96.0, Di=48.0, tc=0.625):
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
        self.tc = tc
        self._casing = VoidedShaft(D=self.Di, Di=self.Di - 2.0*self.tc)


    def __str__(self):
        return "Composite %d inch diameter drilled shaft with %d inch diameter void with %.3f-inch thick casing" % (self.D, self.Di, self.tc)

    @property
    def casing(self):
        "We have to build the casing every time in case D, Di, or tc was changed"
        _casing = VoidedShaft(D=self.Di, Di=self.Di - 2.0*self.tc)
        _casing.c = self.c - (self.D - self.Di)/2.0/self.concrete.beta1()
        return _casing
        
        
