"Structural analysis of FDOT demonstration shaft. (2018)"
#!/usr/bin/env python3
import os

from matplotlib import pyplot as plt

from models.voidedshaft import VoidedShaft
from views.voidedshaft_views import plot_interaction_diagram, plot_voided_shaft

if __name__ == "__main__":
    # Information from Sargent & Lundy calculation number TEC-S-G-006, Rev. 0
    shaft = VoidedShaft(D=9.0*12, Di=0.0)
    shaft.n = 36
    shaft.steel.fy = 60000.0
    shaft.concrete.fc = 4000.0
    shaft.cover = 6.0
    shaft.set_bar_size("#9")
    shaft.set_tiebar_size("#5")

    plot_voided_shaft(shaft)
    plt.savefig(os.path.join("docs/images", "demo-shaft-unvoided.png"))

    plt.clf()
    shaft.Di = 48.0
    phiMn_max, phiPn_max = plot_interaction_diagram(shaft, label="Voided shaft")
    shaft.Di = 0.0
    phiMn_max, phiPn_max = plot_interaction_diagram(shaft, label="Equivalent solid shaft")

    # Add titles and save
    plt.legend()
    plt.savefig(os.path.join("docs/images", "demo-shaft-interaction.png"))

    plt.scatter(5200.0, 30.0, label="Worst-Case Real-World Load Combination")
    plt.legend()
    plt.savefig(os.path.join("docs/images", "real-world-demo-shaft-interaction.png"))

    plt.clf()
    plot_voided_shaft(shaft)
    plt.savefig(os.path.join("docs/images", "demo-shaft-voided.png"))
