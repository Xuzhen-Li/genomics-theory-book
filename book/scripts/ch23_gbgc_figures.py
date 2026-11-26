"""Chapter 23 figure: equilibrium GC content under mutation bias and GC-biased gene conversion.

Usage: python -B ch23_gbgc_figures.py OUTDIR
Deterministic calculation, no random numbers. Mutation from G or C to A or T happens lam times as often as the
reverse. GC-biased gene conversion acts like weak selection for G and C alleles with population-scaled
strength B = 4 Ne b, where b is the transmission bias per heterozygote. With Kimura fixation probabilities the
ratio of AT-to-GC to GC-to-AT substitution rates is exp(B) / lam, so the equilibrium GC content is
GC* = 1 / (1 + lam exp(-B)). Curves are drawn for lam = 1, 2 and 4.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
B = np.linspace(0, 6, 601)
cols = {1: bs.GREY_TXT, 2: bs.BLUE, 4: bs.ORANGE}
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for lam in (1, 2, 4):
    gc = 1 / (1 + lam * np.exp(-B))
    print("lam = %d: GC* at B = 0 %.3f, B = 1 %.3f, B = 3 %.3f" % (lam, gc[0], gc[100], gc[300]))
    a1.plot(B, gc, color=cols[lam], lw=1.2, label="GC-to-AT mutation %d times AT-to-GC" % lam)
a1.set_xlim(0, 6); a1.set_ylim(0, 1.3)
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("Strength of biased conversion, B = 4 Ne b")
a1.set_ylabel("Equilibrium GC content")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Mutation pulls towards AT", "Without conversion bias, GC content\nsettles where mutation puts it,\nbelow one half if GC-to-AT dominates", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Conversion pushes towards GC", "In heterozygotes G and C alleles are\ntransmitted more often, so regions\nwith more crossovers gain GC", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Ne and recombination set B", "Large populations, many crossovers\nand outcrossing raise B; selfing\nand clonal growth lower it", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig23_2_gc_equilibrium"))
