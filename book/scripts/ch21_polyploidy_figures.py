"""Chapter 21 figure: why a polyploid lineage with lower net diversification is usually, but not always, lost.

Usage: python -B ch21_polyploidy_figures.py OUTDIR
Deterministic calculation, no random numbers. A lineage starts as one species and follows a constant-rate
birth-death process with speciation rate lam and extinction rate mu (per million years). The probability that
it still has living species after t million years is (lam - mu) / (lam - mu * exp(-(lam - mu) t)), which tends
to 1 - mu / lam. The diploid lineage has lam = 0.20, mu = 0.10; the polyploid lineage has lower speciation and
higher extinction, lam = 0.15, mu = 0.14, in the direction reported by Mayrose et al. (2011). The rates are
illustrative and are not estimates for any clade.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
def surv(lam, mu, t):
    r = lam - mu
    return r / (lam - mu * np.exp(-r * t))
t = np.linspace(0, 100, 1001)
dip = surv(0.20, 0.10, t)
pol = surv(0.15, 0.14, t)
for T in (10, 50, 100):
    i = int(T * 10)
    print("t = %d My: diploid %.3f, polyploid %.3f" % (T, dip[i], pol[i]))
print("limits: diploid %.3f, polyploid %.3f" % (1 - 0.10 / 0.20, 1 - 0.14 / 0.15))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
a1.plot(t, dip, color=bs.BLUE, lw=1.2, label="diploid: speciation 0.20, extinction 0.10")
a1.plot(t, pol, color=bs.ORANGE, lw=1.2, label="polyploid: speciation 0.15, extinction 0.14")
a1.axhline(0.5, color=bs.BLUE, lw=0.6, ls=":")
a1.axhline(1 - 0.14 / 0.15, color=bs.ORANGE, lw=0.6, ls=":")
a1.set_xlim(0, 100); a1.set_ylim(0, 1.3)
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("Time since origin (million years)")
a1.set_ylabel("Probability the lineage survives")
a1.legend(frameon=False, loc="upper right", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Most new polyploids are lost", "With lower speciation and higher\nextinction, a new polyploid lineage\nusually leaves no living species", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "A few survive and radiate", "Survival is not zero; ancient\nduplications in living plants come\nfrom these rare successes", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Rates are hard to estimate", "Model artefacts, missed cytotypes\nand lags after duplication change\nthe estimated rates", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig21_2_lineage_survival"))
