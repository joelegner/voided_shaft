#!/usr/bin/env python3
import math


class Donut:
    def __init__(self, r1, r2):
        self.r1 = max(r1, r2)
        self.r2 = min(r1, r2)


def intersect_circle(r, y):
    "Returns 0, 1, or 2 points crossed by horizontal line at y"
    if r*r - y*y < 0:
        x = 0.0
    else:
        x = math.sqrt(r*r - y*y)
    return (-x, x)


def intersect_donut(donut, y):
    "Returns 0, 1, 2, 3, or 4 points crossed by horizontal line at y"
    x1, x2 = intersect_circle(donut.r1, y)
    x3, x4 = intersect_circle(donut.r2, y)
    return (x1, x2, x3, x4)


def err(val, actual):
    return round((actual - val)/actual*100.0, 1)


if __name__ == "__main__":
    h = 16.0
    h0 = 8.0
    NUM_SLICES = 100
    dy = h/NUM_SLICES

    A = 0.0
    I = 0.0

    shaft = Donut(r1=h/2.0, r2=h0/2.0)

    for i in range(0, NUM_SLICES + 1):
        y = i*h/NUM_SLICES - h/2.0
        x1, x2, x3, x4 = intersect_donut(shaft, y)
        # print(i, x1, x2, x3, x4)
        dA = (x2 - x1)*dy - (x4 - x3)*dy
        A = A + dA
        I = I + dA*y*y

    real_A = math.pi*h*h/4.0 - math.pi*h0*h0/4.0
    print("A = ", A, real_A, 100*(A - real_A)/real_A)
    print(err(A, real_A))
    real_I = math.pi/4.0*(h/2.0)**4 - math.pi/4.0*(h0/2.0)**4
    print("I = ", I, real_I, 100*(I - real_I)/real_I)

