import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os
os.makedirs("/home/xander/stonehenge_repo/visualizations", exist_ok=True)
print("Creating visualizations...")
fig, ax = plt.subplots(figsize=(16, 6))
stages = [
    (3000, 2620, "Stage 1\nBank/Ditch + Aubrey 56", "#8B4513"),
    (2620, 2480, "Stage 2\nTrilithons + Sarsen Circle +\nDouble Bluestone Circle (PEAK)", "#2E8B57"),
    (2480, 2280, "Stage 3\nBluestonehenge to Central Circle\nAvenue built", "#4682B4"),
    (2280, 2020, "Stage 4\nBluestone Oval + Outer Circle", "#DAA520"),
    (2020, 1520, "Stage 5\nY/Z Holes, Rock Art,\nBluestone Fragmentation", "#CD5C5C"),
]
for year, label, color in events:
    plt.axvline(year, color=color, linestyle="--", alpha=0.5, linewidth=1.5)
    plt.text(year, 0.7, label, rotation=90, va="bottom", ha="center", fontsize=8, color=color, fontweight="bold")
plt.xlim(3200, 1400)
plt.ylim(-0.5, 1.2)
plt.xlabel("Year (cal BC)", fontsize=12, fontweight="bold")
plt.title("Stonehenge Chronology: 5-Stage Construction Sequence (Darvill et al. 2012, 62 14C dates, Bayesian OxCal)", fontsize=14, fontweight="bold")
plt.yticks([])
plt.gca().invert_xaxis()
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("/home/xander/stonehenge_repo/visualizations/01_chronology.png", dpi=300, bbox_inches="tight")
plt.close()
print("1/12: Chronology done")
