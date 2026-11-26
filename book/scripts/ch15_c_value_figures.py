"""Chapter 15 figures: genome size set by a balance of transposable element gain and DNA loss.

Usage: python -B ch15_c_value_figures.py OUTDIR
Stochastic simulation, seed 20261126, time steps of 10000 years over 10 million years. Every lineage has the
same 60 Mb of genes and other single-copy DNA. Repeat DNA R grows by transposable element insertions, drawn
each step as a Poisson number of events (mean 0.5 per step) of exponential size (mean 1 Mb, so 50 Mb per
million years on average), and shrinks by small deletions that remove a fixed fraction of the repeat DNA per
step, set by its half-life. Lineage A has a repeat half-life of 1 million years, lineage B of 20 million years.
Lineage C is A plus one burst of 600 Mb of new copies at 4 million years. Each lineage starts at its
deterministic equilibrium R* = (insertion rate) / (deletion rate).
"""
import os, sys, math
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
GENES, STEP, T = 60.0, 0.01, 10.0
steps = int(T / STEP + 0.5)
t = np.arange(steps + 1) * STEP
def lineage(half_life, burst=None):
    d = 1 - 0.5 ** (STEP / half_life)
    ins = 0.5 * 1.0
    r = ins / d
    out_ = [GENES + r]
    for i in range(1, steps + 1):
        k = rng.poisson(0.5)
        r = r * (1 - d) + rng.exponential(1.0, size=k).sum()
        if burst is not None and abs(t[i] - burst[0]) < STEP / 2:
            r += burst[1]
        out_.append(GENES + r)
    return np.array(out_)
A = lineage(1.0)
B = lineage(20.0)
C = lineage(1.0, burst=(4.0, 600.0))
for lab, x in (("A", A), ("B", B), ("C", C)):
    print(lab, "start %.0f Mb, at 4.5 My %.0f Mb, end %.0f Mb, repeat share at end %.2f" % (x[0], x[450], x[-1], 1 - GENES / x[-1]))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
a1.plot(t, B, color=bs.BLUE, lw=1.1, label="B: slow DNA loss (half-life 20 My)")
a1.plot(t, C, color=bs.ORANGE, lw=1.1, label="C: as A, with a burst at 4 My")
a1.plot(t, A, color=bs.GREEN, lw=1.1, label="A: fast DNA loss (half-life 1 My)")
a1.axhline(GENES, color=bs.GREY_TXT, lw=0.8, ls=":", label="genes and single-copy DNA (60 Mb)")
a1.set_yscale("log"); a1.set_ylim(40, 20000); a1.set_xlim(0, 10)
a1.set_yticks([50, 100, 200, 500, 1000, 2000]); a1.set_yticklabels(["50", "100", "200", "500", "1000", "2000"])
a1.minorticks_off()
a1.set_xlabel("Time (million years)"); a1.set_ylabel("Haploid genome size (Mb, log scale)")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Same genes, different sizes", "All three lineages carry the same\ngenes; the size differences are\nall repeat DNA", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Gain against loss", "Size settles where insertions balance\ndeletions: R* = insertion / deletion rate", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Bursts fade", "A burst of new copies can double a\ngenome or more in a short time; deletion\nbias then removes it over a few half-lives", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig15_2_genome_size_balance"))
