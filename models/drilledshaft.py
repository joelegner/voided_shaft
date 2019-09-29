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
        pass


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

    def analyze(self):
        # a = depth of compression block
        # c = depth to neutral axis
        # d = depth to centerline of steel

        print("Analyzing drilled shaft")

        CINC = 0.25
        c = 0.125
        # while c <= self.D:
        while c <= 12.0:
            T = 0.0
            C = 0.0
            M = 0.0
            P = 0.0

            print(c)
            for bar_loc in self.bar_locations():
                # Depth to this bar in inches
                d = self.D/2 - bar_loc[1]

                # Bar strain
                epsilon_s = (d - c)*epsilon_c/c

                # Bar yield
                if epsilon_s > 0.0:
                    # Bar is in tension
                    fs = min(epsilon_s*self.steel.E, self.steel.fy)
                    print("Bar at (%.2f, %.2f) has strain = %.4f and stress fy = %.0f" % (
                        bar_loc[0], bar_loc[1], epsilon_s, fs))
                    T = T + self.bar.Ab*fs
                    M = M + T*(d - c)
                else:
                    # Bar is in compression
                    fs = max(-epsilon_s*self.steel.E, self.steel.fy)
                    print("Bar at (%.2f, %.2f) has strain = %.4f and stress fy = %.0f" % (
                        bar_loc[0], bar_loc[1], epsilon_s, fs))
                    C = C + self.bar.Ab*fs
                    M = M + C*(d - c)
                P = P + C - T

            c = c + CINC
