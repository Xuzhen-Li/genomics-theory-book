"""Chapter 26 figure: the dominance explanation of Haldane’s rule in its simplest form.

Usage: python -B ch26_sex_chromosome_figures.py OUTDIR
Deterministic calculation, no random numbers. In an F1 hybrid every autosomal locus is heterozygous. The X
is heterozygous in XX hybrids but hemizygous in XY hybrids. Each hybrid incompatibility allele harms a
heterozygous carrier with weight h (its dominance) and a hemizygous carrier with weight 1. If a fraction x of
these alleles sit on the X, the expected harm to XY hybrids divided by the harm to XX hybrids is
(1 - x) + x / h. Curves are drawn for x = 0.1, 0.2 and 0.3. Interactions between loci, faster evolution of
X-linked genes and sex-specific genes are left out, so the values are illustrative.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
h = np.linspace(0.05, 1, 476)
cols = {0.1: bs.GREY_TXT, 0.2: bs.BLUE, 0.3: bs.ORANGE}
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for x in (0.1, 0.2, 0.3):
    r = (1 - x) + x / h
    print("x = %.1f: ratio at h = 0.05 %.2f, h = 0.1 %.2f, h = 0.25 %.2f, h = 0.5 %.2f, h = 1 %.2f" % (x, r[0], r[25], r[100], r[225], r[-1]))
    a1.plot(h, r, color=cols[x], lw=1.2, label="%d%% of incompatibility alleles on the X" % int(100 * x + 0.5))
a1.axhline(1, color=bs.GREY_TXT, lw=0.6, ls=":")
a1.text(0.98, 1.25, "equal harm to both sexes", ha="right", va="bottom", fontsize=6.5, color=bs.GREY_TXT)
a1.set_xlim(0, 1); a1.set_ylim(0, 10)
a1.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_yticks([0, 2, 4, 6, 8])
a1.set_xlabel("Dominance of incompatibility alleles, h")
a1.set_ylabel("Harm to XY hybrids / harm to XX")
a1.legend(frameon=False, loc="upper right", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Recessive alleles are exposed", "An XY hybrid shows every X-linked\nincompatibility in full; an XX hybrid\nmasks them when they are recessive", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "The same logic in ZW species", "Birds and butterflies have ZW\nfemales, and there the females are\nthe hybrids that fail first", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Plants test it", "Dioecious plants such as Silene\nhave young X and Y; most crops are\nhermaphrodite and cannot show it", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig26_2_haldane_dominance"))
