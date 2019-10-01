import math
import os
import unittest

from matplotlib import pyplot as plt

from leglib.structural.acibars import a615_grade60, bars
from leglib.structural.concrete import Concrete
from leglib.util import almost_equal
from models.drilledshaft import DrilledShaft
from views.drilledshaft_views import plot_drilled_shaft


def plot_interaction(shaft, filename="interaction-diagram.png"):

    plt.clf()

    SEGMENTS = 400

    xs = [0.0]
    ys = [shaft.phiPnmax()/1000.0]

    shaft.c = shaft.D*1.5

    phiPn_max = 0.0
    phiMn_max = 0.0

    while (shaft.D - 2.0*shaft.a)/shaft.D < 1.0:

        if (shaft.D - 2.0*shaft.a)/shaft.D < -1.0:
            shaft.c = shaft.c - shaft.D/SEGMENTS
            continue

        phiMn = shaft.phiMn()/1000.0
        phiPn = shaft.phiPn()/1000.0

        print("c = {}, phiMn = {}, phiPn = {}".format(shaft.c, phiMn, phiPn))

        xs.append(phiMn)
        ys.append(phiPn)
        phiPn_max = max(phiPn_max, phiPn)
        phiMn_max = max(phiMn_max, phiMn)

        shaft.c = shaft.c - shaft.D/SEGMENTS

    plt.plot(xs, ys)

    plt.scatter(1645.0, 1004.0, color="red")
    plt.scatter(2353.0, 0.0, color="red")
    plt.scatter(2487.0, 789.0, color="red")
    plt.scatter(2794.0, 638.0, color="red")
    plt.scatter(2913.0, 523.0, color="red")
    plt.scatter(2927.0, 333.0, color="red")

    plt.title(
        "Agreement Between Python Program\nand 2008 CRSI Example on p. 4-7")

    plt.savefig(os.path.join("output", filename))

    return (phiMn_max, phiPn_max)


if __name__ == "__main__":
    test_shaft = DrilledShaft(D=20.0)
    test_shaft.n = 6
    test_shaft.bar = bars["#9"]
    test_shaft.cover = 1.5
    test_shaft.tiebar = bars["#3"]
    test_shaft.concrete.fc = 6000.0
    test_shaft.c = 20.51791
    phiMn_max, phiPn_max = plot_interaction(test_shaft, "interaction.png")
    plot_drilled_shaft(test_shaft, "test_shaft.png")
    print("Maximum phiMn = {} and maximum phiPn = {}".format(phiMn_max, phiPn_max))
