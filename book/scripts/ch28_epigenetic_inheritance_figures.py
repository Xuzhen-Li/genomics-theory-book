"""Chapter 28 figure: how long an induced epiallele lasts when methylation is gained and lost at random.

Usage: python -B ch28_epigenetic_inheritance_figures.py OUTDIR
Deterministic calculation, no random numbers. At one cytosine, methylation is gained with probability a and
lost with probability b each generation, so the methylated fraction of a lineage follows
m(t + 1) = m(t)(1 - b) + (1 - m(t)) a and approaches a / (a + b). Curves start from a site fully methylated
by an induced change (m = 1) and run for 10 000 generations with a = 1e-4 and b = 5e-4 (blue) or 5e-3
(orange). For comparison, a DNA mutation with a rate of 1e-8 per generation hardly changes in that time
(grey). The values are illustrative and chosen to show the shape of the curves.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
T = 10000
t = np.arange(0, T + 1)


def run(a, b):
    m = np.empty(T + 1); m[0] = 1.0
    for i in range(T):
        m[i + 1] = m[i] * (1 - b) + (1 - m[i]) * a
    return m


fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for a, b, c, lab in ((1e-4, 5e-4, bs.BLUE, "epiallele, loss 5e-4 per generation"), (1e-4, 5e-3, bs.ORANGE, "epiallele, loss 5e-3 per generation"), (0.0, 1e-8, bs.GREY_TXT, "DNA allele, mutation 1e-8")):
    m = run(a, b)
    print("%s: m at t = 10 %.4f, 100 %.4f, 1000 %.4f, 10000 %.4f; equilibrium %.4f" % (lab, m[10], m[100], m[1000], m[T], a / (a + b)))
    a1.plot(t[1:], m[1:], color=c, lw=1.2, label=lab)
a1.set_xscale("log")
a1.set_xlim(1, T); a1.set_ylim(0, 1.3)
a1.set_xticks([1, 10, 100, 1000, 10000]); a1.set_xticklabels(["1", "10", "100", "1 000", "10 000"])
a1.xaxis.set_minor_locator(plt.NullLocator())
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("Generations after the induced change")
a1.set_ylabel("Chance the site is still methylated")
a1.legend(frameon=False, loc="upper right", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Epialleles drift back", "Random gain and loss pull every site\ntowards a balance, so an induced\nstate fades over generations", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Faster than DNA change", "Epimutation rates are far higher\nthan DNA mutation rates, so\nepialleles are less stable", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Clones carry marks along", "Cuttings and grafts avoid the reset\nof meiosis and seed, so somatic\nmarks can pass between clones", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig28_2_epiallele_decay"))
