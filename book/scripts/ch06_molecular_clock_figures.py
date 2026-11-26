"""Chapter 6 figures: strict versus relaxed clock, and two models of how per-year rates scale with generation time.

Usage: python -B ch06_molecular_clock_figures.py OUTDIR
Seed 20261126. (a) 150 lineage pairs with divergence times uniform on 5-100 Myr, 1000 sites,
rate 1e-3 substitutions per site per Myr per lineage. Strict clock: Poisson counts. Relaxed clock:
each lineage rate multiplied by a lognormal factor (sigma 0.5, mean 1).
(b) Illustration only: per-year rate if mutations track generations (slope -1 on log scales)
versus if they track absolute time (flat). Reference point: 7e-9 per site per generation at 1 year.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
NP, SITES, RATE = 150, 1000, 1e-3
t = rng.uniform(5, 100, NP)
strict = rng.poisson(2 * RATE * SITES * t) / SITES
sig = 0.5
f = rng.lognormal(-sig ** 2 / 2, sig, (NP, 2)).sum(axis=1) / 2
relaxed = rng.poisson(2 * RATE * SITES * t * f) / SITES
for name, d in (("strict", strict), ("relaxed", relaxed)):
    resid = d - 2 * RATE * t
    print("%s: residual SD %.4f" % (name, resid.std()))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(150 * bs.MM, 64 * bs.MM))
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.2, top=0.88, wspace=0.34)
tt = np.array([0, 105])
a1.plot(tt, 2 * RATE * tt, color="#333333", lw=0.8, ls="--", label="expected, constant rate")
a1.plot(t, relaxed, "o", ms=2.6, color=bs.ORANGE, alpha=0.9, mec="none", label="relaxed (lognormal rates)")
a1.plot(t, strict, "o", ms=2.6, color=bs.BLUE, alpha=0.9, mec="none", label="strict (Poisson only)")
a1.set_xlim(0, 105); a1.set_ylim(0, 0.42); a1.set_yticks([0, 0.1, 0.2, 0.3, 0.4])
a1.set_xlabel("Divergence time (Myr)"); a1.set_ylabel("Pairwise distance (subst. per site)")
a1.legend(frameon=False, loc="upper left")
G = np.logspace(0, 2, 50)
mu_g = 7e-9
a2.plot(G, mu_g / G, color=bs.BLUE, lw=1.4, label="mutations track generations")
a2.plot(G, np.full_like(G, mu_g), color=bs.ORANGE, lw=1.4, label="mutations track years")
a2.plot(G, mu_g / np.sqrt(G), color=bs.PURPLE, lw=1.2, ls="--", label="partial compensation")
a2.set_xscale("log"); a2.set_yscale("log"); a2.minorticks_off()
a2.set_xlim(1, 100); a2.set_ylim(3e-11, 3e-8)
a2.set_xticks([1, 3, 10, 30, 100]); a2.set_xticklabels(["1", "3", "10", "30", "100"])
a2.set_yticks([1e-10, 1e-9, 1e-8]); a2.set_yticklabels(["1e-10", "1e-9", "1e-8"])
a2.set_xlabel("Generation time (years)"); a2.set_ylabel("Mutations per site per year")
a2.legend(frameon=False, loc="lower left")
for a, l in ((a1, "a"), (a2, "b")):
    a.text(-0.2, 1.04, l, transform=a.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig06_2_clock_models"))
