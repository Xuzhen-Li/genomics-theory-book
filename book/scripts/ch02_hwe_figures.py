"""Chapter 2 figures: heterozygosity under random mating and four departures; reading a departure.

Usage: python -B ch02_hwe_figures.py OUTDIR
Seed 20261126. 200 diploid individuals per locus, 120 loci per scenario.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
N, L = 200, 120

def sample(p, F):
    """Genotype counts with inbreeding coefficient F (negative F = heterozygote excess)."""
    het = 2 * p * (1 - p) * (1 - F)
    hom1 = p * p + F * p * (1 - p)
    probs = np.clip([hom1, het, 1 - hom1 - het], 0, None); probs = probs / probs.sum()
    g = rng.multinomial(N, probs)
    pa = (2 * g[0] + g[1]) / (2 * N)
    return pa, g[1] / N

res = {}
ps = rng.uniform(0.05, 0.95, L)
res["Random mating"] = [sample(p, 0.0) for p in ps]
res["Selfing 60% (F = 0.43)"] = [sample(p, 0.6 / (2 - 0.6)) for p in ps]
wl = []
for p in ps:
    d = min(0.2, p - 0.01, 0.99 - p)
    a = sample(p - d, 0.0); b = sample(p + d, 0.0)
    wl.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2))
res["Wahlund mixture"] = wl
pcl = rng.uniform(0.2, 0.8, L)
res["Clonal (F = -0.4)"] = [sample(p, -0.4) for p in pcl]
par = []
for p in rng.uniform(0.02, 0.48, L):
    # two collapsed paralogs: one fixed for allele 1, the other segregating at frequency q
    q = p * 2
    g = rng.binomial(2, q, N)
    obs_het = np.mean((g < 2))  # any copy differing from the fixed paralog appears heterozygous
    pa = (2 * N + 2 * g.sum()) / (4 * N)
    par.append((1 - pa, obs_het))
res["Collapsed paralogs"] = par

cols = {"Random mating": ("#333333", "o"), "Selfing 60% (F = 0.43)": (bs.BLUE, "s"),
        "Wahlund mixture": (bs.GREEN, "^"), "Clonal (F = -0.4)": (bs.ORANGE, "D"),
        "Collapsed paralogs": (bs.RED, "v")}
fig, ax = plt.subplots(figsize=(120 * bs.MM, 85 * bs.MM))
fig.subplots_adjust(left=0.11, right=0.70, bottom=0.14, top=0.96)
x = np.linspace(0, 1, 200)
ax.plot(x, 2 * x * (1 - x), color="#000000", lw=1.2, zorder=1, label="2pq (expected)")
for k, v in res.items():
    v = np.array(v)
    ax.scatter(v[:, 0], v[:, 1], s=9, marker=cols[k][1], facecolor=cols[k][0], edgecolor="#333333",
               linewidth=0.3, alpha=0.85, zorder=2, label=k)
ax.set_xlim(0, 1); ax.set_ylim(0, 1.06)
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xlabel("Allele frequency p"); ax.set_ylabel("Observed heterozygosity")
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), frameon=False, handletextpad=0.3, borderaxespad=0.2)
bs.save(fig, os.path.join(out, "fig02_2_heterozygosity_departures_sim"))

# Figure 2.3: reading a departure
fig = plt.figure(figsize=(183 * bs.MM, 80 * bs.MM))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off(); ax.set_xticks([]); ax.set_yticks([])
bs.panel(ax, 0.30, 0.78, 0.40, 0.19, "Locus departs from HWE",
       "First check: exact test, multiple testing, power", fc=bs.GREY_LIGHT)
bs.panel(ax, 0.02, 0.30, 0.30, 0.40, "Heterozygote deficit (F > 0)",
       "Many loci: selfing, inbreeding,\nor Wahlund effect (structure)\nFew loci: null alleles, allele dropout,\nlow depth, selection", fc=bs.BLUE_BG)
bs.panel(ax, 0.35, 0.30, 0.30, 0.40, "Heterozygote excess (F < 0)",
       "Many loci: clonality, small number\nof parents, outbreeding\nFew loci: collapsed paralogs,\nheterozygote advantage", fc=bs.RED_BG)
bs.panel(ax, 0.68, 0.30, 0.30, 0.40, "Sex- or ploidy-specific",
       "X-linked: use males as well\nPolyploids: model dosage and\ndouble reduction\nHaplodiploids: separate sexes", fc=bs.GREY_LIGHT)
bs.panel(ax, 0.02, 0.03, 0.96, 0.21, "Technical checks before biology",
       "Does F track read depth or missingness?   Are heterozygote read ratios far from 0.5?\n"
       "Are clones, synonyms or relatives in the sample?   Does the pattern hold within each genetic cluster?", fc="#FFFFFF")
for xe in (0.17, 0.50, 0.83):
    ax.annotate("", xy=(xe, 0.705), xytext=(0.5, 0.78), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="#333333", lw=0.6, shrinkA=0, shrinkB=0))
bs.save(fig, os.path.join(out, "fig02_3_reading_departures_schematic"))
