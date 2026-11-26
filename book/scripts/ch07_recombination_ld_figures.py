"""Chapter 7 figures: expected LD decay under drift and recombination, and how to read an LD decay plot.

Usage: python -B ch07_recombination_ld_figures.py OUTDIR
No random numbers. Sved (1971) expectation E[r2] = 1 / (1 + 4 N c), plus 1/n for a finite sample
(a common approximation). rho = 4 N c per kb. Selfing scales c by (1 - F); F = 0.95 is used here.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
d = np.linspace(0, 100, 500)
n = 50
cases = [("outcrossing, rho = 1 per kb", 1.0, bs.BLUE, "-"),
         ("same, selfing F = 0.95", 1.0 * 0.05, bs.ORANGE, "-"),
         ("small Ne, rho = 0.02 per kb", 0.02, bs.PURPLE, "--")]
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for lab, rho, col, ls in cases:
    r2 = 1 / (1 + rho * d) + 1 / n
    a1.plot(d, r2, color=col, lw=1.4, ls=ls, label=lab)
    half = (1 / 0.5 - 1) / rho
    print("%s: r2 halves (without sample term) at %.1f kb" % (lab, half))
a1.axhline(1 / n, color=bs.GREY_TXT, lw=0.7, ls=":")
a1.text(98, 1 / n + 0.07, "sample floor 1/n (n = 50)", color=bs.GREY_TXT, ha="right", fontsize=7)
a1.set_xlim(0, 100); a1.set_ylim(0, 1.05); a1.set_yticks([0, 0.25, 0.5, 0.75, 1])
a1.set_xlabel("Distance between SNPs (kb)"); a1.set_ylabel("Expected r\u00b2")
a1.legend(frameon=False, loc="upper right")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Reading the curve", "Decay distance scales with 4Nc, not c;\nselfing and bottlenecks stretch it", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Inflated LD, not linkage", "Structure, admixture and relatedness\nraise r\u00b2 between distant SNPs", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Compare like with like", "Same n, same MAF filter, same\nmarkers; report the r\u00b2 floor", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig07_2_ld_decay"))
