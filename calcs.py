#!/usr/bin/env python3
from models.drilledshaft import DrilledShaft
import math

shaft = DrilledShaft(D=9*12)
shaft.analyze()
print(shaft.steel)
print(shaft.steel.ey)
