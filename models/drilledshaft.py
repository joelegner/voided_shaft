#!/usr/bin/env python3
from leglib.structural.acibars import bars
from leglib.structural.concrete import Concrete
from leglib.structural.acibars import a615_grade60
import math

# Ultimate concrete strain
epsilon_c = 0.003


class DrilledShaft:

    def __init__(self, D=96.0):
        """
        D = diameter in inches
        """
        self.D = D
        self.n = 24
        self.bar = bars["#10"]
        self.tiebar = bars["#4"]
        self.cover = 6.0
        self.concrete = Concrete(4000.0)
        self.steel = a615_grade60
        self.c = 1.0

    def __str__(self):
        return "%d inch diameter drilled shaft" % self.D

    def intersect_circle(self, r, y):
        "Returns 0, 1, or 2 points crossed by horizontal line at y"
        if r*r - y*y < 0:
            x = 0.0
        else:
            x = math.sqrt(r*r - y*y)
        return (-x, x)

    def bar_circle_radius(self):
        "Returns radius of bar circle in inches"
        return self.D/2.0 - self.cover - self.bar.db/2.0 - self.tiebar.db

    def bar_locations(self):
        "Returns a tuple of (x, y) coordinates for the bars"
        locations = []

        for i in range(0, self.n):
            theta = i*math.radians(360.0)/self.n
            x = math.cos(theta)*self.bar_circle_radius()
            y = math.sin(theta)*self.bar_circle_radius()
            locations.append((x, y))

        return tuple(locations)

    def _dsi(self):
        "Returns bar locations list"
        return [self.D/2.0 - y for x, y in self.bar_locations()]

    def _esi(self):
        "Returns bar strains list"
        return [self.concrete.ec*(1.0 - dsi/self.c) for dsi in self._dsi()]

    def _fsi(self):
        "Returns bar stress list"
        return [max(-self.steel.fy, min(self.steel.fy, self.steel.E*esi)) for esi in self._esi()]

    def _theta(self):
        "Return value of theta in radians"
        return math.asin((self.D - 2.0*self.c)/self.D)

    def _gamma(self):
        "Return value of gamma in radians"
        return math.asin(1 - self.concrete.beta1() + self.concrete.beta1()*math.sin(self._theta()))

    def _z(self):
        gamma = self._gamma()
        theta = self._theta()
        return -math.cos(gamma) + (gamma - (math.pi/2.0))*math.sin(theta) + math.cos(theta)*(math.log((1 - math.tan(theta/2.0)*math.tan(gamma/2.0))/(math.tan(gamma/2.0) - math.tan(theta/2.0))))

    @property
    def a(self):
        return self.concrete.beta1()*self.c

    def alpha(self):
        return math.acos((self.D - 2.0*self.a)/self.D)

    def Ac(self):
        h = self.D
        alpha = self.alpha()
        return h**2*(2.0*alpha - math.sin(2*alpha))/8.0

    def ybar(self):
        "Returns distance of concrete centroid from column centroid at y=c"
        h = self.D
        alpha = self.alpha()
        return (2.0*h**3)*math.sin(alpha)**3/(24.0*self.Ac())

    def Cc(self):
        "Returns compression resultant in pounds"
        # Based upon CRSI handbook 2008, page 4-7
        return 0.85*self.concrete.fc*self.Ac()

    def Mc(self):
        "Returns moment caused by compression zone only in lb-in"
        return self.Cc()*self.ybar()

    def _Fsi(self):
        "Returns a list of bar forces in pounds"
        Fsi = []
        fsis = self._fsi()
        locs = self.bar_locations()
        for i in range(0, self.n):
            fsi = fsis[i]
            y = locs[i][1]
            if (self.D/2.0 - y) < self.a:
                # Reduce contribution of bar by the amount of concrete displaced
                Fsi.append((fsi - 0.85*self.concrete.fc)*self.bar.Ab)
            else:
                Fsi.append(fsi*self.bar.Ab)
        return Fsi

    def _Pns(self):
        "Returns axial force caused by the steel in pounds"
        return sum(self._Fsi())

    def _Pnc(self):
        "Returns axial force caused by the concrete compression in pounds"
        return self.Cc()

    def _Msi(self):
        dsis = self._dsi()
        Fsis = self._Fsi()
        assert(len(dsis) == len(Fsis))
        assert(len(dsis) == self.n)
        Msi = []
        for i in range(0, len(dsis)):
            dsi = dsis[i]
            Fsi = Fsis[i]
            Msi.append(Fsi*(self.D/2.0 - dsi))
        return Msi

    def Mn(self):
        return sum(self._Msi()) + self.Mc()

    def phiMn(self):
        return self.phi()*self.Mn()

    def Pn(self):
        "Returns nominal axial capacity in pounds"
        return self._Pns() + self._Pnc()

    def phi(self):
        # maximum steel strain (compare magnitude only)
        es_max = math.fabs(min(self._esi()))
        es_comp = self.steel.fy/self.steel.E
        phi = 0.65 + (0.90 - 0.65)/(0.005 - es_comp)*(es_max - es_comp)
        return min(0.90, max(0.65, phi))

    def phiPn(self):
        "Returns axial capacity in pounds"
        return min(self.phi()*self.Pn(), self.phiPnmax())

    def _Qc(self):
        h = self.D
        fc = self.concrete.fc
        theta = self._theta()
        gamma = self._gamma()
        z = self._z()
        return h**3*math.sqrt(fc)/810.0*(1.0 - math.sin(theta))*(math.pi/4.0 - gamma/2.0 - math.sin(2*gamma)/4.0 + z*math.sin(theta))

    def _cc(self):
        return self._Qc()/self._Ac()

    def _Ic(self):
        h = self.D
        fc = self.concrete.fc
        theta = self._theta()
        gamma = self._gamma()
        z = self._z()
        return h**4*math.sqrt(fc)/1621.0*(1.0 - math.sin(theta))*((math.cos(gamma)**3/3.0) + math.sin(theta)*(math.pi/4.0 - gamma/2.0 - math.sin(2.0*gamma)/4.0 + z*math.sin(theta)))

    @property
    def Ag(self):
        "Returns gross area in square inches"
        return math.pi*self.D**2/4.0

    @property
    def Ast(self):
        "Returns area of steel in square inches"
        return self.n*self.bar.Ab

    def phiPnmax(self):
        "Return Pn(max) in pounds, assuming it is a tied column"
        phi = 0.65  # Tied column
        return phi*0.80*(0.85*self.concrete.fc*(self.Ag - self.Ast) + self.steel.fy*self.Ast)
