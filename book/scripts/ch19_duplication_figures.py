"""Chapter 19 figures: how often a new gene duplicate is kept by subfunctionalization.

Usage: python -B ch19_duplication_figures.py OUTDIR
Monte Carlo, seed 20261126, 20000 duplicate pairs per point. Each copy has a coding region and z independent
regulatory subfunctions. Fixed degenerative mutations arrive one at a time: in a working copy, a null mutation
of the coding region (relative rate 1) or the loss of one of its subfunctions (relative rate r per
subfunction). A mutation is fixed only if every subfunction is still carried by at least one working copy;
otherwise it is removed by selection and ignored. A pair ends as non-functionalized when one copy becomes a
null, or as subfunctionalized when each copy carries at least one subfunction that the other has lost, so that
both are needed. No new functions arise. z runs from 1 to 8 and r is 0.25, 1 or 4.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
REPS = 20000
def p_sub(z, r):
    sub = 0
    for _ in range(REPS):
        have = np.ones((2, z), dtype=bool)
        while True:
            w = np.concatenate([[1.0], r * have[0], [1.0], r * have[1]])
            e = rng.choice(w.size, p=w / w.sum())
            c, j = (0, e) if e <= z else (1, e - z - 1)
            if j == 0:
                if have[1 - c].all():
                    break
                continue
            k = j - 1
            if not have[1 - c, k]:
                continue
            have[c, k] = False
            u0 = (have[0] & ~have[1]).any(); u1 = (have[1] & ~have[0]).any()
            if u0 and u1:
                sub += 1; break
    return sub / REPS
Z = np.arange(1, 9)
res = {}
for r in (0.25, 1.0, 4.0):
    res[r] = np.array([p_sub(z, r) for z in Z])
    print("r = %.2f:" % r, " ".join("%.3f" % v for v in res[r]))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for r, col, mk in ((4.0, bs.ORANGE, "s"), (1.0, bs.BLUE, "o"), (0.25, bs.GREEN, "^")):
    a1.plot(Z, res[r], color=col, lw=1.0, marker=mk, ms=3.5, label="subfunction loss %g x null rate" % r)
a1.set_xlim(0.5, 8.5); a1.set_ylim(0, 1.32)
a1.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
a1.set_xticks(Z)
a1.set_xlabel("Independent subfunctions per gene (z)")
a1.set_ylabel("Probability both copies are kept")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Usual fate: loss", "A null mutation in either copy is\nharmless at first; where nulls are\ncommon, most copies become pseudogenes", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Complementary losses", "If each copy first loses a different\nsubfunction, both become essential\nwithout any new function", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Not in this model", "Partial losses, new functions, drift\nand population size change these\nprobabilities", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig19_2_subfunctionalization"))
