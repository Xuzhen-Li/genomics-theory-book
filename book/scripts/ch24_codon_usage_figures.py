"""Chapter 24 figure: the selection-mutation-drift model of codon usage (Bulmer 1991).

Usage: python -B ch24_codon_usage_figures.py OUTDIR
Deterministic calculation, no random numbers. For a two-codon amino acid, mutation to the unpreferred codon
happens kappa = 2 times as often as the reverse, and the preferred codon has a selective advantage s that
rises in proportion to expression, s = s0 x with s0 = 1e-7 and x the relative expression level. The expected
frequency of the preferred codon is Fop = 1 / (1 + kappa exp(-4 Ne s)). Curves are drawn for Ne = 1e6, 2e5
and 2e4. The values are illustrative.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
KAPPA, S0 = 2.0, 1e-7
x = np.logspace(-1, 2, 601)
cols = {1e6: bs.BLUE, 2e5: bs.ORANGE, 2e4: bs.GREY_TXT}
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for ne in (1e6, 2e5, 2e4):
    fop = 1 / (1 + KAPPA * np.exp(-4 * ne * S0 * x))
    print("Ne = %.0e: Fop at x = 0.1 %.3f, x = 1 %.3f, x = 10 %.3f, x = 100 %.3f" % (ne, fop[0], fop[200], fop[400], fop[600]))
    a1.plot(x, fop, color=cols[ne], lw=1.2, label="Ne = %s" % {1e6: "1 000 000", 2e5: "200 000", 2e4: "20 000"}[ne])
a1.axhline(1 / (1 + KAPPA), color=bs.GREY_TXT, lw=0.6, ls=":")
a1.set_xscale("log")
a1.set_xlim(0.1, 100); a1.set_ylim(0, 1.3)
a1.set_xticks([0.1, 1, 10, 100]); a1.set_xticklabels(["0.1", "1", "10", "100"])
a1.xaxis.set_minor_locator(plt.NullLocator())
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("Relative expression level of the gene")
a1.set_ylabel("Frequency of preferred codon")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Mutation sets the floor", "Weakly expressed genes keep the\ncodon mix that mutation bias gives\n(dotted line)", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Selection rises with expression", "Highly expressed genes gain more\nfrom accurate, efficient translation,\nso they use preferred codons more", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Ne decides if it shows", "The same benefit is visible in large\npopulations and lost to drift in small\nones, such as many selfers", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig24_2_codon_selection"))
