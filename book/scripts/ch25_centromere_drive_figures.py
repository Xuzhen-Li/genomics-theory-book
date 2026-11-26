"""Chapter 25 figure: a driving centromere held in check by a recessive fitness cost.

Usage: python -B ch25_centromere_drive_figures.py OUTDIR
Deterministic calculation, no random numbers. A driving allele D is transmitted to a fraction k of the eggs
of heterozygous females and to half the sperm or pollen of heterozygous males. Plants homozygous for D have
their fertility reduced by a fraction s in both sexes; heterozygotes pay no cost. Egg and pollen pools are
followed separately and the recursion is run for 20 000 generations from a starting frequency of 0.01. The
curves show the frequency of D that the population settles at, for k = 0.55, 0.58 and 0.65. The grey band
marks the 32-40% frequency of a 58:42 driver observed in a wild Mimulus guttatus population (Fishman and
Kelly 2015). The cost model is a simplification and the values are illustrative.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
s = np.linspace(0, 1, 501)


def settle(k, s, gens=20000):
    pf = np.full_like(s, 0.01); pm = np.full_like(s, 0.01)
    for _ in range(gens):
        dd = pf * pm; dh = pf * (1 - pm) + pm * (1 - pf); nn = (1 - pf) * (1 - pm)
        w = dd * (1 - s) + dh + nn
        pf = (dd * (1 - s) + dh * k) / w
        pm = (dd * (1 - s) + dh * 0.5) / w
    return (pf + pm) / 2


cols = {0.55: bs.GREY_TXT, 0.58: bs.BLUE, 0.65: bs.ORANGE}
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
a1.axhspan(0.32, 0.40, color=bs.GREY_LIGHT, lw=0)
a1.text(0.98, 0.36, "observed in Mimulus", ha="right", va="center", fontsize=6.5, color=bs.GREY_TXT)
for k in (0.55, 0.58, 0.65):
    p = settle(k, s)
    print("k = %.2f: D frequency at s = 0.1 %.3f, s = 0.3 %.3f, s = 0.6 %.3f, s = 1 %.3f" % (k, p[50], p[150], p[300], p[500]))
    a1.plot(s, p, color=cols[k], lw=1.2, label="drive in females %d:%d" % (int(100 * k + 0.5), 100 - int(100 * k + 0.5)))
a1.set_xlim(0, 1); a1.set_ylim(0, 1.3)
a1.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("Fitness cost to DD homozygotes, s")
a1.set_ylabel("Frequency of driving allele D")
a1.legend(frameon=False, loc="upper right", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Drive needs asymmetric meiosis", "Only one product of female meiosis\nbecomes the egg, so a centromere that\nwins that position spreads", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Costs stop it fixing", "If DD plants pay a price, D settles at\nan intermediate frequency instead\nof replacing the other allele", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Clones escape the contest", "Plants grown from cuttings skip\nmeiosis, so drive acts only in the\nseedling generations of breeding", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig25_2_centromere_drive"))
