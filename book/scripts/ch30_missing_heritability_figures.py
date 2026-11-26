"""Chapter 30 figure: how much heritability genome-wide significant hits capture as GWAS sample size grows.

Usage: python -B ch30_missing_heritability_figures.py OUTDIR
Deterministic calculation, no random numbers. A trait with SNP heritability h2 = 0.5 is spread over M
independent causal variants (M = 1 000, 10 000 or 100 000). The variance q explained by each variant is
exponentially distributed with mean h2 / M. In a GWAS of N people a variant is counted as found when its
expected test statistic N * q reaches the genome-wide threshold c = z**2 for a two-sided P = 5e-8 (about 50%
power). The share of h2 carried by found variants is then (1 + x) * exp(-x) with x = c * M / (N * h2).
The values are illustrative; real effect-size distributions have heavier tails and linkage disequilibrium.
"""
import os, sys
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
H2 = 0.5
C = NormalDist().inv_cdf(1 - 2.5e-8) ** 2
N = np.logspace(3, 7, 400)


def captured(m, nn):
    x = C * m / (nn * H2)
    return (1 + x) * np.exp(-x)


print("threshold c = %.2f" % C)
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for m, col, lab in ((1000, bs.GREEN, "1 000 causal variants"), (10000, bs.BLUE, "10 000 causal variants"), (100000, bs.ORANGE, "100 000 causal variants")):
    f = captured(m, N)
    pts = [captured(m, v) for v in (1e4, 1e5, 1e6, 1e7)]
    print("M = %d: share of h2 found at N = 1e4 %.3f, 1e5 %.3f, 1e6 %.3f, 1e7 %.3f" % ((m,) + tuple(pts)))
    a1.plot(N, f, color=col, lw=1.2, label=lab)
a1.set_xscale("log")
a1.set_xlim(1e3, 1e7); a1.set_ylim(0, 1.3)
a1.set_xticks([1e3, 1e4, 1e5, 1e6, 1e7]); a1.set_xticklabels(["1 000", "10 000", "100 000", "1 million", "10 million"])
a1.xaxis.set_minor_locator(plt.NullLocator())
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("GWAS sample size (people)")
a1.set_ylabel("Share of SNP heritability in hits")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Hidden, not missing", "With many small effects, hits\ncapture little heritability until\nsamples become very large", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "More variants, slower gain", "Spreading the same heritability\nover more variants shifts the\ncurve to larger samples", fc=bs.GREY_LIGHT)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "What it leaves out", "Rare variants, poor tagging and\nbiased family estimates also\nopen a gap between estimates", fc=bs.RED_BG)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig30_2_gwas_capture"))
