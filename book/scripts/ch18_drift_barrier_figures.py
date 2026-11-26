"""Chapter 18 figures: the drift barrier to lower mutation rates.

Usage: python -B ch18_drift_barrier_figures.py OUTDIR
Deterministic calculation, no random numbers. The genome-wide deleterious mutation rate U takes values on a
ladder U_k = 1e-9 * 1.25^k (k = 0..110). Mutations in replication or repair genes move a lineage one step up
(worse fidelity) four times as often as one step down. A step from U_k to U_k-1 carries a selective advantage
s_k = c (U_k - U_k-1), where c is the share of the extra load that stays linked to the modifier allele:
c = 1 for full linkage (asexual) and c = 0.05 for a freely recombining genome. Steps are fixed with the
diploid fixation probability P(s) = (1 - exp(-2s)) / (1 - exp(-4 Ne s)). The ladder is a birth-death chain;
the plotted value is the mean of U under its stationary distribution, for Ne from 1e3 to 1e9.
The ratio of fixation probabilities P(-s) / P(s) = exp(-2 s (2 Ne - 1)) is used directly.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
K, U0, R, BIAS = 110, 1e-9, 1.25, 4.0
U = U0 * R ** np.arange(K + 1)
def pfix(s, ne):
    s = np.asarray(s, dtype=float)
    x = -4.0 * ne * s
    num = -np.expm1(-2.0 * s)
    den = -np.expm1(x)
    small = np.abs(x) < 1e-12
    return np.where(small, 1.0 / (2.0 * ne), num / np.where(small, 1.0, den))
def mean_u(ne, c):
    s = c * (U[1:] - U[:-1])
    # log of (BIAS * P(-s)) / P(s); P(-s) / P(s) = exp(-2 s (2 Ne - 1)) exactly
    logp = np.concatenate([[0.0], np.cumsum(np.log(BIAS) - 2.0 * s * (2.0 * ne - 1.0))])
    p = np.exp(logp - logp.max()); p /= p.sum()
    return float((p * U).sum())
NE = 10 ** np.linspace(3, 9, 49)
lin = np.array([mean_u(n, 1.0) for n in NE])
rec = np.array([mean_u(n, 0.05) for n in NE])
for n, a, b in zip(NE[::8], lin[::8], rec[::8]):
    print("Ne %.0e  U linked %.2e  U recombining %.2e" % (n, a, b))
sl = np.polyfit(np.log10(NE[8:40]), np.log10(lin[8:40]), 1)[0]
sr = np.polyfit(np.log10(NE[8:40]), np.log10(rec[8:40]), 1)[0]
print("log-log slopes over Ne 1e4-1e8: linked %.3f, recombining %.3f" % (sl, sr))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
a1.plot(NE, rec, color=bs.BLUE, lw=1.2, label="recombining genome (c = 0.05)")
a1.plot(NE, lin, color=bs.ORANGE, lw=1.2, label="fully linked genome (c = 1)")
a1.plot(NE, 3.0 / NE, color=bs.GREY_TXT, lw=0.8, ls=":", label="slope -1")
a1.set_xscale("log"); a1.set_yscale("log")
a1.set_xlim(1e3, 1e9); a1.set_ylim(1e-9, 1e2)
a1.set_yticks([1e-8, 1e-6, 1e-4, 1e-2, 1])
a1.set_xticks([1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]); a1.minorticks_off()
a1.set_xlabel("Effective population size Ne")
a1.set_ylabel("Mean deleterious mutation rate U\n(per genome per generation)")
a1.legend(frameon=False, loc="upper right", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Selection pushes down", "Each gain in fidelity lowers the load,\nso selection favours lower rates", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Drift sets the floor", "Once the gain of a further step is\nbelow about 1/Ne, drift and biased\nmutation win; U falls roughly as 1/Ne", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Linkage matters", "With recombination, a modifier keeps\nonly part of the load it causes, so the\nfloor is higher at every Ne", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig18_2_drift_barrier"))
