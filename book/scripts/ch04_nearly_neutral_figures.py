"""Chapter 4 figure: Kimura fixation probability and the nearly neutral share under gamma DFEs.

Usage: python -B ch04_nearly_neutral_figures.py OUTDIR
Seed 20261126. Panel b uses 2,000,000 gamma draws per shape (no scipy needed).
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)

S = np.linspace(-10, 10, 801)
with np.errstate(divide="ignore", invalid="ignore"):
    rel = np.where(np.abs(S) < 1e-9, 1.0, S / (1 - np.exp(-S)))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(150 * bs.MM, 64 * bs.MM))
fig.subplots_adjust(left=0.12, right=0.98, bottom=0.19, top=0.89, wspace=0.36)
a1.axvspan(-1, 1, color=bs.GREY_LIGHT, zorder=0)
a1.plot(S, rel, color=bs.BLUE, lw=1.5)
a1.axhline(1, color=bs.GREY_TXT, lw=0.6, ls="--")
a1.set_yscale("log"); a1.set_xlim(-10, 10); a1.set_ylim(1e-4, 30)
a1.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1, 10]); a1.set_yticklabels(["0.0001", "0.001", "0.01", "0.1", "1", "10"])
a1.minorticks_off()
a1.set_xlabel("4Ns"); a1.set_ylabel("Fixation prob. relative to neutral")
a1.text(0, 3e-4, "nearly\nneutral", ha="center", va="center", fontsize=7, color="#000000")
a1.text(-9.3, 2.0, "neutral = 1", fontsize=7, color=bs.GREY_TXT, ha="left")

Ne = np.logspace(3, 7, 41)
for shape, col, tcol, lab_i, dy in ((0.2, bs.RED, bs.RED, 8, 1.4), (0.4, bs.PURPLE, bs.PURPLE, 10, 1.4)):
    s = rng.gamma(shape, 0.01 / shape, 2_000_000)
    share = np.array([np.mean(s < 1 / (4 * n)) for n in Ne])
    a2.plot(Ne, share, color=col, lw=1.5)
    a2.text(Ne[lab_i], share[lab_i] * dy, "gamma shape %.1f" % shape, color=tcol, fontsize=7,
            ha="left", va="center")
a2.set_xscale("log"); a2.set_yscale("log")
a2.set_xlim(1e3, 1e7); a2.set_ylim(0.005, 1)
a2.set_xticks([1e3, 1e4, 1e5, 1e6, 1e7]); a2.set_xticklabels(["1,000", "10,000", "100,000", "1e6", "1e7"])
a2.set_yticks([0.01, 0.03, 0.1, 0.3, 1]); a2.set_yticklabels(["0.01", "0.03", "0.1", "0.3", "1"])
a2.minorticks_off()
a2.set_xlabel("Effective population size Ne"); a2.set_ylabel("Share of mutations with |4Ns| < 1")
for a, l in ((a1, "a"), (a2, "b")):
    a.text(-0.24, 1.04, l, transform=a.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig04_2_fixation_and_dfe"))
