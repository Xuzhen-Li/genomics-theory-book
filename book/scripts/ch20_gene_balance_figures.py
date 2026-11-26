"""Chapter 20 figures: reciprocal retention of dosage-sensitive genes after whole-genome and small-scale duplication.

Usage: python -B ch20_gene_balance_figures.py OUTDIR
Deterministic calculation, no random numbers. Duplicate pairs lose one copy at a neutral rate of 0.1 per
million years, multiplied by the ratio of the fixation probability of the loss to that of a neutral change,
4 Ne s / (exp(4 Ne s) - 1) for a loss with fitness effect -s and 4 Ne s / (1 - exp(-4 Ne s)) for one with +s.
After a whole-genome duplication, losing one copy of a dosage-sensitive gene (one whose product is part of a
complex or network) unbalances it, s = 1e-4 against the loss. After a small-scale duplication of such a gene
the extra copy is the imbalance, so its loss is favoured with the same s. Dosage-insensitive genes are neutral
in both cases. Ne = 1e4, so 4 Ne s = 4. The plot shows the expected share of pairs still duplicated.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
LAM, NE, S = 0.1, 1e4, 1e-4
X = 4 * NE * S
against = X / np.expm1(X)
favoured = X / -np.expm1(-X)
t = np.linspace(0, 40, 401)
wgd_sens = np.exp(-LAM * against * t)
neutral = np.exp(-LAM * t)
ssd_sens = np.exp(-LAM * favoured * t)
print("loss-rate factors: against %.3f, favoured %.3f" % (against, favoured))
for T in (10, 20, 40):
    i = int(T * 10)
    print("t = %d My: WGD sensitive %.3f, neutral %.3f, SSD sensitive %.4f" % (T, wgd_sens[i], neutral[i], ssd_sens[i]))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
a1.plot(t, wgd_sens, color=bs.BLUE, lw=1.2, label="dosage-sensitive, after WGD")
a1.plot(t, neutral, color=bs.GREY_TXT, lw=1.0, ls="--", label="dosage-insensitive, either kind")
a1.plot(t, ssd_sens, color=bs.ORANGE, lw=1.2, label="dosage-sensitive, after SSD")
a1.set_xlim(0, 40); a1.set_ylim(0, 1.32)
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xlabel("Time since duplication (million years)")
a1.set_ylabel("Share of pairs still duplicated")
a1.legend(frameon=False, loc="upper right", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Balance is kept after WGD", "Doubling every gene keeps the ratios;\nlosing one copy of a complex member\nbreaks them, so such losses are rare", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Balance is broken by SSD", "A single extra copy of a complex\nmember is the imbalance, so its loss\nis favoured", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Reciprocal retention", "The same genes are over-retained\nafter WGD and under-retained after\nSSD; neutral genes behave alike", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig20_2_reciprocal_retention"))
