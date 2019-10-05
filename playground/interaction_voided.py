import math
import os
import unittest

from matplotlib import pyplot as plt

from leglib.structural.acibars import a615_grade60, bars
from leglib.structural.concrete import Concrete
from leglib.util import almost_equal
from models.voidedshaft import VoidedShaft
from views.voidedshaft_views import plot_voided_shaft


def plot_interaction(shaft):

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

        # print("c = {}, phiMn = {}, phiPn = {}".format(shaft.c, phiMn, phiPn))

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
    return (phiMn_max, phiPn_max)


if __name__ == "__main__":
    test_shaft = VoidedShaft(D=20.0, Di=12.0)
    test_shaft.n = 6
    test_shaft.bar = bars["#9"]
    test_shaft.cover = 1.5
    test_shaft.tiebar = bars["#3"]
    test_shaft.concrete.fc = 6000.0
    test_shaft.c = 20.51791

    # Draw a cross-section
    cross_section_filename = "voided-test-shaft.png"
    plot_voided_shaft(test_shaft, cross_section_filename)

    # Plot results with void first
    plt.clf()
    phiMn_max, phiPn_max = plot_interaction(test_shaft)

    # Re-run same shaft without void and plot over top of same diagram
    test_shaft.Di = 0.0
    phiMn_max, phiPn_max = plot_interaction(test_shaft)

    # Add titles and save
    plt.title("Voided Shaft\nand 2008 CRSI Example on p. 4-7")
    plt.savefig(os.path.join("output", "interaction-voided.png"))

    # print("Maximum phiMn = {} and maximum phiPn = {}".format(phiMn_max, phiPn_max))
