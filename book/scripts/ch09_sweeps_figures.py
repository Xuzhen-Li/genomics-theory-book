"""Chapter 9 figures: how likely a sweep from recurrent mutation is soft, and what hard and soft sweeps leave behind.

Usage: python -B ch09_sweeps_figures.py OUTDIR
No random numbers. With recurrent beneficial mutation at population-scaled rate theta = 4 Ne u (u per copy per
generation at the target), the number of independent origins of the adaptive allele in a sample of n copies
taken at fixation follows the Ewens sampling formula (Pennings and Hermisson 2006). The probability that the
sample carries a single origin (a hard sweep in the sample) is prod_{i=1}^{n-1} i / (i + theta).
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
theta = np.logspace(-3, 2, 400)
def p_hard(n, th):
    i = np.arange(1, n)[:, None]
    return np.prod(i / (i + th[None, :]), axis=0)
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for n, col, ls in [(2, bs.ORANGE, "--"), (10, bs.BLUE, "-"), (100, bs.PURPLE, "-")]:
    ps = 1 - p_hard(n, theta)
    a1.plot(theta, ps, color=col, lw=1.4, ls=ls, label="sample of n = %d" % n)
    print("n=%d: P(soft) at theta 0.01 %.3f, 0.1 %.3f, 1 %.3f" % (n, np.interp(0.01, theta, ps), np.interp(0.1, theta, ps), np.interp(1, theta, ps)))
a1.set_xscale("log"); a1.minorticks_off()
a1.set_xlim(1e-3, 100); a1.set_xticks([1e-3, 1e-2, 0.1, 1, 10, 100]); a1.set_xticklabels(["0.001", "0.01", "0.1", "1", "10", "100"])
a1.set_ylim(0, 1.3); a1.set_yticks([0, 0.25, 0.5, 0.75, 1])
a1.set_xlabel("Population-scaled beneficial mutation rate, \u03b8 = 4Neu")
a1.set_ylabel("P(sample shows more than one origin)")
a1.legend(frameon=False, loc="upper left")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Hard sweep", "One haplotype rises; deep trough in\ndiversity; excess rare and high-frequency\nderived alleles; high H1 and H12", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Soft sweep", "Several haplotypes carry the allele\n(standing variation or recurrent mutation);\nshallow trough; high H12 and H2/H1", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Confounders", "Bottlenecks, background selection and\nincomplete or old sweeps mimic either\nsignature; use a fitted demographic null", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig09_2_soft_sweep_probability"))
