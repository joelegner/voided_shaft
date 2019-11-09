from leglib import reportmaker
import math
import matplotlib.pyplot as plt
from leglib import fmt
import os

# Write the homework asginment. Pass it the local variable dict, the names we want in our context,
# and the template filename.
context = {}

reportmaker.make_report_from_context(context, "report.md")
