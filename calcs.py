#!/usr/bin/env python3
import math
import os

from matplotlib import pyplot as plt

from models.voidedshaft import VoidedShaft
from views.voidedshaft_views import plot_interaction_diagram, plot_voided_shaft

if __name__ == "__main__":
    # Information from Sargent & Lundy calculation number TEC-S-G-006, Rev. 0
    shaft = VoidedShaft(D=108.0, Di=0.0)
    shaft.n = 30
    shaft.steel.fy = 60000.0
    shaft.concrete.fc = 4000.0
    shaft.cover = 3.0
    shaft.set_bar_size("#11")
    shaft.set_tiebar_size("#4")

    plot_voided_shaft(shaft, filename="sargent-lundy-shaft.png")

    plt.clf()
    phiMn_max, phiPn_max = plot_interaction_diagram(shaft)
    shaft.Di = 48.0
    phiMn_max, phiPn_max = plot_interaction_diagram(shaft)

    # Add point from run
    plt.scatter((5196.0*12.0), 30.0, label="S&L Design")

    # Add titles and save
    plt.title("P-M Diagram for S&L Shaft")
    plt.savefig(os.path.join("output", "interaction-sargent-lundy.png.png"))

    plt.clf()
    plot_voided_shaft(shaft, filename="sargent-lundy-shaft-voided.png")
