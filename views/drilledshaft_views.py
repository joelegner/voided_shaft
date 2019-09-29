#!/usr/bin/env python3
from matplotlib import pyplot as plt
import os


def plot_drilled_shaft(shaft, filename="drilledshaft.png"):
    circle = plt.Circle((0.0, 0.0), shaft.D/2,
                        fill=False, edgecolor='darkgrey')
    ax = plt.gca()
    ax.add_patch(circle)
    plot_rebar(plt, shaft)
    plt.axis('scaled')
    plt.savefig(os.path.join("output", filename))


def plot_rebar(plt, shaft):
    # Plot ties
    ties_circle = plt.Circle((0.0, 0.0), shaft.D/2 -
                             shaft.cover, fill=False, edgecolor='black')
    plt.gca().add_patch(ties_circle)
    ties_circle = plt.Circle((0.0, 0.0), shaft.D/2 -
                             shaft.cover - shaft.tiebar.db, fill=False, edgecolor='black')
    plt.gca().add_patch(ties_circle)

    # Plot axial bars
    for loc in shaft.bar_locations():
        bar_circle = plt.Circle(
            (loc[0], loc[1]), radius=shaft.bar.db/2, fill=True, color='black')
        plt.gca().add_patch(bar_circle)
