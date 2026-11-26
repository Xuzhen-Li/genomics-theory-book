"""Chapter 16 figures: how the mutational load limits the functional fraction of the human genome.

Usage: python -B ch16_junk_dna_figures.py OUTDIR
Deterministic calculation, no random numbers, in the spirit of Graur (2017). A diploid zygote receives
U = 2 * G * u * f * p new deleterious mutations, with haploid genome size G = 3.1e9 bp, point mutation rate
u = 1.2e-8 per bp per generation, functional fraction f, and p the share of mutations in functional DNA
that are deleterious. At mutation-selection balance with multiplicative effects mean fitness is exp(-U)
(Haldane-Muller principle, independent of the size of the effects), so a population that is to keep its size
needs on average 2 * exp(U) births per woman, before any other cause of death. The two reference lines mark
the 8.2% of the genome that Rands et al. (2014) estimated to be under constraint and the 80% that ENCODE
(2012) called biochemically functional.
"""
import os, sys, math
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
G, u = 3.1e9, 1.2e-8
f = np.linspace(0.0, 1.0, 201)
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for p, col in ((0.2, bs.RED), (0.1, bs.ORANGE), (0.05, bs.BLUE)):
    U = 2 * G * u * f * p
    births = 2 * np.exp(U)
    a1.plot(f * 100, births, color=col, lw=1.2, label="p = %.2f deleterious" % p)
    for ff in (0.082, 0.25, 0.8):
        UU = 2 * G * u * ff * p
        print("p=%.2f f=%.3f U=%.2f births=%.1f" % (p, ff, UU, 2 * math.exp(UU)))
a1.axvline(8.2, color=bs.GREEN_TXT, lw=0.9, ls="--")
a1.axvline(80, ymin=0.45, color=bs.GREY_TXT, lw=0.9, ls="--")
a1.text(9.5, 3e4, "8.2% constrained", color=bs.GREEN_TXT, fontsize=6.5, va="top")
a1.text(81.5, 3e4, "80%\nENCODE", color=bs.GREY_TXT, fontsize=6.5, va="top")
a1.set_yscale("log"); a1.set_ylim(1, 1e5); a1.set_xlim(0, 100)
a1.set_yticks([1, 10, 100, 1000, 10000, 100000]); a1.set_yticklabels(["1", "10", "100", "1000", "10000", "100000"]); a1.minorticks_off()
a1.set_xlabel("Functional fraction of the genome, f (%)"); a1.set_ylabel("Births per woman needed")
a1.legend(frameon=False, loc="lower right")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Function means vulnerability", "DNA that matters can be damaged by\nmutation; the more of it, the more new\nharmful mutations every child carries", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "80% is hard to sustain", "With 80% functional the required\nbirths per woman reach the tens to\nthe hundreds even for small p", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Assumptions", "Multiplicative effects, point mutations\nonly, fixed u and G; synergistic\nepistasis or soft selection lower the cost", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig16_2_mutational_load_limit"))
