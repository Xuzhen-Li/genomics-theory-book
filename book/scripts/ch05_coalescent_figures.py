"""Chapter 5 figures: coalescent times and site frequency spectra, and what the standard coalescent assumes.

Usage: python -B ch05_coalescent_figures.py OUTDIR
Seed 20261126. Kingman coalescent, time in units of 2N generations (diploid), sample n = 10.
Expansion model: population size 10x larger for t < 0.5, size 1 before (piecewise constant).
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
N_SAMPLE, REPS = 10, 20000


def genealogy(n, sizes):
    """Return (tmrca, branch length per number of descendants) for one coalescent tree.
    sizes: list of (start_time, relative_size), piecewise constant, sorted by start_time."""
    lineages = [1] * n
    t = 0.0
    seg = 0
    L = np.zeros(n)
    while len(lineages) > 1:
        k = len(lineages)
        rate = k * (k - 1) / 2 / sizes[seg][1]
        w = rng.exponential(1 / rate)
        nxt = sizes[seg + 1][0] if seg + 1 < len(sizes) else np.inf
        if t + w > nxt:
            for d in lineages:
                L[d] += nxt - t
            t = nxt
            seg += 1
            continue
        for d in lineages:
            L[d] += w
        t += w
        i, j = sorted(rng.choice(k, 2, replace=False))
        merged = lineages[i] + lineages[j]
        del lineages[j]
        lineages[i] = merged
    return t, L[1:]


const = [(0.0, 1.0)]
expand = [(0.0, 10.0), (0.5, 1.0)]
res_c = [genealogy(N_SAMPLE, const) for _ in range(REPS)]
res_e = [genealogy(N_SAMPLE, expand) for _ in range(REPS)]
tm_c = np.array([r[0] for r in res_c])
sfs_c = np.mean([r[1] for r in res_c], axis=0)
sfs_e = np.mean([r[1] for r in res_e], axis=0)
sfs_c, sfs_e = sfs_c / sfs_c.sum(), sfs_e / sfs_e.sum()
i = np.arange(1, N_SAMPLE)
neutral = (1 / i) / np.sum(1 / i)
print("mean TMRCA %.3f expected %.3f" % (tm_c.mean(), 2 * (1 - 1 / N_SAMPLE)))
print("singleton share constant %.3f expansion %.3f expected %.3f" % (sfs_c[0], sfs_e[0], neutral[0]))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(150 * bs.MM, 62 * bs.MM))
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.2, top=0.88, wspace=0.32)
a1.hist(tm_c, bins=np.linspace(0, 6, 49), color=bs.BLUE, alpha=0.85, density=True)
a1.axvline(2 * (1 - 1 / N_SAMPLE), color="#333333", lw=0.9, ls="--")
a1.text(2.0, 0.66, "expected 2(1 - 1/n) = 1.8", fontsize=7, ha="left", va="center")
a1.set_xlim(0, 6); a1.set_ylim(0, 0.75); a1.set_yticks([0, 0.2, 0.4, 0.6])
a1.set_xlabel("Time to most recent common ancestor (2N generations)"); a1.set_ylabel("Density")
w = 0.38
a2.bar(i - w / 2, sfs_c, width=w, color=bs.BLUE, label="constant size")
a2.bar(i + w / 2, sfs_e, width=w, color=bs.ORANGE, label="recent 10x expansion")
a2.plot(i, neutral, "o", color="#333333", ms=3, label="expected 1/i")
a2.set_xticks(i); a2.set_xlim(0.4, 9.6); a2.set_ylim(0, 0.6); a2.set_yticks([0, 0.2, 0.4, 0.6])
a2.set_xlabel("Derived allele count i (n = 10)"); a2.set_ylabel("Share of segregating sites")
a2.legend(frameon=False, loc="upper right")
for a, l in ((a1, "a"), (a2, "b")):
    a.text(-0.2, 1.04, l, transform=a.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig05_2_coalescent_times_sfs_sim"))

fig = plt.figure(figsize=(150 * bs.MM, 82 * bs.MM))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off(); ax.set_xticks([]); ax.set_yticks([])
ax.text(0.03, 0.95, "Standard coalescent assumption", fontsize=8, fontweight="bold", va="top", transform=ax.transAxes)
ax.text(0.52, 0.95, "When it fails, what you see", fontsize=8, fontweight="bold", va="top", transform=ax.transAxes)
rows = [("One random-mating population", "Structure: false size changes in PSMC plots"),
        ("Constant population size", "Growth: excess singletons, negative Tajima D"),
        ("Neutral sites, no linked selection", "Linked selection distorts local trees"),
        ("Small variance in offspring number", "Multiple mergers: the Kingman shape breaks down"),
        ("No recombination inside the locus", "Many local trees along the genome (ARG, SMC)")]
y = 0.86
for a, b in rows:
    bs.panel(ax, 0.03, y - 0.13, 0.44, 0.13, a, fc=bs.BLUE_BG, bsize=7)
    bs.panel(ax, 0.52, y - 0.13, 0.45, 0.13, b, fc=bs.RED_BG, tsize=7.5)
    ax.annotate("", xy=(0.515, y - 0.065), xytext=(0.475, y - 0.065), xycoords=ax.transAxes,
                arrowprops=dict(arrowstyle="->", color="#333333", lw=0.7))
    y -= 0.165
bs.save(fig, os.path.join(out, "fig05_3_coalescent_assumptions_schematic"))
