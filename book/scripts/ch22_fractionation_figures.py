"""Chapter 22 figure: biased fractionation after an allopolyploid whole-genome duplication.

Usage: python -B ch22_fractionation_figures.py OUTDIR
Deterministic calculation, no random numbers. Each ancestral gene starts as a pair, one copy in each
subgenome. Pairs are resolved by losing one copy at rate k = 0.05 per million years, so the share still in
pairs is exp(-k t). When a copy is lost it comes from the less expressed (recessive) subgenome with
probability b and from the dominant subgenome with probability 1 - b. Biased case: b = 0.62 (about 1.6 losses
in the recessive subgenome for each loss in the dominant one); unbiased case: b = 0.5. The share of ancestral
genes kept in the dominant subgenome is P + (1 - P) b and in the recessive subgenome P + (1 - P)(1 - b),
with P = exp(-k t). Loss of both copies is ignored. The values are illustrative.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
K, BIAS = 0.05, 0.62
t = np.linspace(0, 80, 801)
P = np.exp(-K * t)
dom = P + (1 - P) * BIAS
rec = P + (1 - P) * (1 - BIAS)
unb = P + (1 - P) * 0.5
for T in (12, 40, 80):
    i = int(T * 10)
    print("t = %d My: pairs %.3f, dominant %.3f, recessive %.3f, unbiased %.3f, ratio %.2f" % (T, P[i], dom[i], rec[i], unb[i], dom[i] / rec[i]))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
a1.plot(t, dom, color=bs.BLUE, lw=1.2, label="dominant subgenome, biased loss")
a1.plot(t, rec, color=bs.ORANGE, lw=1.2, label="recessive subgenome, biased loss")
a1.plot(t, unb, color=bs.GREY_TXT, lw=1.0, ls="--", label="either subgenome, unbiased loss")
a1.plot(t, P, color=bs.GREEN, lw=0.9, ls=":", label="genes still in pairs")
a1.set_xlim(0, 80); a1.set_ylim(0, 1.35)
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("Time since duplication (million years)")
a1.set_ylabel("Share of ancestral genes kept")
a1.legend(frameon=False, loc="upper right", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Fractionation", "After duplication most pairs lose\none copy, mostly by short deletions,\nand the genome returns to diploidy", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Biased fractionation", "If losses fall more often on one\nsubgenome, the other keeps more\ngenes and is called dominant", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Not universal", "Some duplications, often thought\nto be autopolyploid, show no clear\nbias between subgenomes", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig22_2_biased_fractionation"))
