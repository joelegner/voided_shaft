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
        return "%d inch diameter drilled shaft" % self.d

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

    def _Ac(self):
        return self.D**2*math.sqrt(self.concrete.fc)/405.0*(1.0 - math.sin(self._theta()))*self._z()

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
                    print("Bar at (%.2f, %.2f) has strain = %.4f and stress fy = %.0f" % (bar_loc[0], bar_loc[1], epsilon_s, fs))
                    T = T + self.bar.Ab*fs
                    M = M + T*(d - c)
                else:
                    # Bar is in compression
                    fs = max(-epsilon_s*self.steel.E, self.steel.fy)
                    print("Bar at (%.2f, %.2f) has strain = %.4f and stress fy = %.0f" % (bar_loc[0], bar_loc[1], epsilon_s, fs))
                    C = C + self.bar.Ab*fs
                    M = M + C*(d - c)
                P = P + C - T

            c = c + CINC

if __name__ == "__main__":
    from leglib.util import almost_equal
    test_shaft = DrilledShaft(D = 16.0)
    test_shaft.n = 8
    test_shaft.bar = bars["#9"]
    test_shaft.cover = 2.5 - test_shaft.bar.db/2.0

    # Test against results in article:
    # Tayem, A. and Najmi, A., "Design of Round Reinforced-Concrete Columns", Journal of Structural Engineering, September 1996

    
    assert(almost_equal(test_shaft.Ag, 201.061929829746767, places=4))

    test_shaft.c = 6.0

    assert(almost_equal(test_shaft.concrete.beta1(), 0.85, places=2))
    assert(almost_equal(test_shaft._theta(), 0.253, places=3))
    assert(almost_equal(test_shaft._gamma(), 0.371, places=3))
    assert(almost_equal(test_shaft._z(), 1.459, places=3))
    assert(almost_equal(test_shaft._Ac(), 43.743, places=3))
    assert(almost_equal(test_shaft._Qc(), 190.867, places=3))
    assert(almost_equal(test_shaft._cc(), 4.363, places=3))
    assert(almost_equal(test_shaft._Ic(), 899.369, places=0))

