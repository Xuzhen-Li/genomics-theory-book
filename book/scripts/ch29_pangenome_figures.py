"""Chapter 29 figure: how a pangenome grows as genomes are added, for open and closed pangenomes.

Usage: python -B ch29_pangenome_figures.py OUTDIR
Deterministic calculation, no random numbers. The first genome contributes G1 = 30 000 genes. The k-th genome
added (k >= 2) brings kappa * k**(-alpha) genes not seen before, with kappa = 4 000. The pangenome after n
genomes is G1 plus the sum of these new genes. With alpha <= 1 the sum keeps growing without limit (an open
pangenome); with alpha > 1 it levels off (a closed pangenome). The core genome shrinks towards a floor as
C(n) = Cinf + (G1 - Cinf) * n**(-0.6), with Cinf = 24 000. The values are illustrative and chosen to show the
shape of the curves, not fitted to any species.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
G1, KAPPA, CINF, NMAX = 30000.0, 4000.0, 24000.0, 100
n = np.arange(1, NMAX + 1)


def pan(alpha):
    new = np.zeros(NMAX)
    new[1:] = KAPPA * n[1:] ** (-alpha)
    return G1 + np.cumsum(new)


core = CINF + (G1 - CINF) * n ** (-0.6)
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for alpha, c, lab in ((0.5, bs.ORANGE, "pangenome, alpha = 0.5 (open)"), (1.0, bs.BLUE, "pangenome, alpha = 1.0"), (1.5, bs.GREEN, "pangenome, alpha = 1.5 (closed)")):
    p = pan(alpha)
    print("alpha %.1f: pangenome at n = 2 %d, 10 %d, 50 %d, 100 %d; genes new in genome 100: %.1f" % (alpha, int(p[1]), int(p[9]), int(p[49]), int(p[99]), KAPPA * NMAX ** (-alpha)))
    a1.plot(n, p / 1000, color=c, lw=1.2, label=lab)
print("core at n = 1 %d, 10 %d, 100 %d" % (int(core[0]), int(core[9]), int(core[99])))
a1.plot(n, core / 1000, color=bs.GREY_TXT, lw=1.2, ls="--", label="core genome")
a1.set_xlim(1, NMAX); a1.set_ylim(20, 120)
a1.set_xticks([1, 20, 40, 60, 80, 100])
a1.set_yticks([20, 40, 60, 80, 100, 120])
a1.set_xlabel("Number of genomes sampled")
a1.set_ylabel("Genes (thousands)")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Open pangenome", "New genes keep turning up with\nevery genome, so one reference\nmisses part of the species", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Closed pangenome", "New genes become rare, and a\nfew dozen genomes capture almost\nthe whole gene repertoire", fc=bs.GREY_LIGHT)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Core genome", "Genes shared by every sample;\nit shrinks as samples are added\nand settles at a floor", fc=bs.RED_BG)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig29_2_pangenome_growth"))
