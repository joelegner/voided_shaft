#!/usr/bin/env python3
from matplotlib import pyplot as plt
import os


def plot_voided_shaft(shaft):
    plt.clf()

    circle_0 = plt.Circle((0.0, 0.0), shaft.D/2.0,
                          fill=False, edgecolor='darkgrey')
    circle_i = plt.Circle((0.0, 0.0), shaft.Di/2.0,
                          fill=False, edgecolor='darkgrey')
    ax = plt.gca()
    ax.add_patch(circle_0)
    ax.add_patch(circle_i)
    plot_rebar(plt, shaft)
    plt.axis('scaled')


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


def plot_interaction_diagram(shaft, label=""):

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

        xs.append(phiMn/12.0)   # Convert to kip-ft
        ys.append(phiPn)
        phiPn_max = max(phiPn_max, phiPn)
        phiMn_max = max(phiMn_max, phiMn)

        shaft.c = shaft.c - shaft.D/SEGMENTS

    plt.xlabel("Moment, $\phi M_n$, kip-ft")
    plt.ylabel("Axial Load, $\phi P_n$, kips")
    plt.plot(xs, ys, label=label)

    return (phiMn_max, phiPn_max)
