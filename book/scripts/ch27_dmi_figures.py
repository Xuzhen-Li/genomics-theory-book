"""Chapter 27 figure: the snowball of Dobzhansky-Muller incompatibilities (Orr 1995).

Usage: python -B ch27_dmi_figures.py OUTDIR
Deterministic calculation, no random numbers. After K substitutions have separated two lineages, the number
of pairs among them is K(K - 1)/2, and in Orr’s model the pairs that can form a hybrid incompatibility grow at
this rate. If each pair is incompatible with a small probability p, the expected number of pairwise
incompatibilities is p K(K - 1)/2, which grows with the square of divergence. Curves are drawn for p = 0.002 and p = 0.001. The
dotted line is a linear model scaled to give the same count as p = 0.001 at K = 100. The values are
illustrative.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
K = np.arange(0, 201)
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for p, c in ((0.002, bs.ORANGE), (0.001, bs.BLUE)):
    n = p * K * (K - 1) / 2
    print("p = %.3f: incompatibilities at K = 50 %.2f, K = 100 %.2f, K = 200 %.2f" % (p, n[50], n[100], n[200]))
    a1.plot(K, n, color=c, lw=1.2, label="pairwise, p = %.3f" % p)
lin = (0.001 * 100 * 99 / 2) / 100 * K
print("linear: at K = 50 %.2f, K = 100 %.2f, K = 200 %.2f" % (lin[50], lin[100], lin[200]))
a1.plot(K, lin, color=bs.GREY_TXT, lw=1.0, ls=":", label="linear accumulation")
a1.set_xlim(0, 200); a1.set_ylim(0, 52)
a1.set_xticks([0, 50, 100, 150, 200])
a1.set_yticks([0, 10, 20, 30, 40])
a1.set_xlabel("Substitutions separating the lineages, K")
a1.set_ylabel("Expected incompatibilities")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "No unfit step is needed", "Each lineage stays fit; the trouble\nappears only when derived alleles\nfrom both meet in a hybrid", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Pairs outrun substitutions", "Untested pairs grow with the square\nof divergence, so isolation should\nsnowball rather than grow linearly", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Plant cases are known", "Immune genes in Arabidopsis and\nsterility loci in rice are mapped\nexamples of such pairs", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig27_2_dmi_snowball"))
