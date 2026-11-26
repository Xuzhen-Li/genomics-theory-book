"""Chapter 10 figures: realised and masked genetic load through a domestication-like bottleneck.

Usage: python -B ch10_genetic_load_figures.py OUTDIR
Wright-Fisher simulation of allele frequencies at independent biallelic loci (no linkage, no epistasis), seed
20261126. Two classes of 5000 loci each, one-way mutation u = 1e-5 per locus per generation to the deleterious
allele: mildly deleterious and additive (s = 0.002, h = 0.5) and strongly deleterious and nearly recessive
(s = 0.5, h = 0.02). Fitnesses 1, 1 - hs, 1 - s. Burn-in of 20000 generations at N = 5000, then a bottleneck of
N = 100 for 2000 generations, then N = 5000 again for 1000 generations. Realised load per class is the sum over loci of
2pq hs + q^2 s; masked load is s pq (1 - 2h), the part that inbreeding would expose. Values are illustrative.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
L, u = 5000, 1e-5
CL = [("mild", 0.002, 0.5), ("strong", 0.5, 0.02)]
q = {k: np.zeros(L) for k, s, h in CL}
def step(N):
    for k, s, h in CL:
        x = q[k] + u * (1 - q[k])
        p = 1 - x
        wbar = p * p + 2 * p * x * (1 - h * s) + x * x * (1 - s)
        x = (p * x * (1 - h * s) + x * x * (1 - s)) / wbar
        q[k] = rng.binomial(2 * N, x) / (2 * N)
def loads():
    r = {}
    for k, s, h in CL:
        x = q[k]; p = 1 - x
        r[k] = (np.sum(2 * p * x * h * s + x * x * s), np.sum(s * p * x * (1 - 2 * h)))
    return r
for g in range(20000):
    step(5000)
T = np.arange(-200, 3001)
rec = []
for t in T:
    rec.append(loads())
    step(100 if 0 <= t < 2000 else 5000)
mild_r = np.array([r["mild"][0] for r in rec]); str_r = np.array([r["strong"][0] for r in rec]); str_m = np.array([r["strong"][1] for r in rec])
for t in (-1, 500, 1999, 2500, 3000):
    i = int(np.where(T == t)[0][0])
    print("t=%d mild realised %.3f strong realised %.3f strong masked %.3f" % (t, mild_r[i], str_r[i], str_m[i]))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.57, 0.44, 0.31])
a3 = fig.add_axes([0.10, 0.17, 0.44, 0.31])
a2 = fig.add_axes([0, 0, 1, 1])
for ax in (a1, a3):
    ax.axvspan(0, 2000, color=bs.GREY_LIGHT, lw=0)
    ax.set_xlim(-200, 3000)
a1.plot(T, mild_r, color=bs.ORANGE, lw=1.4, label="mild, additive")
a1.plot(T, str_r, color=bs.BLUE, lw=1.4, label="strong, recessive")
a1.set_ylim(0, 0.6); a1.set_yticks([0, 0.2, 0.4]); a1.set_ylabel("Realised load")
a1.set_xticklabels([])
a1.text(1000, 0.97 * a1.get_ylim()[1], "bottleneck, N = 100", ha="center", va="top", fontsize=7, color=bs.GREY_TXT)
a1.legend(frameon=False, loc="upper right")
a3.plot(T, str_m, color=bs.BLUE, lw=1.4)
a3.set_ylim(0, 3); a3.set_yticks([0, 1, 2]); a3.set_ylabel("Masked load")
a3.set_xlabel("Generations since the start of the bottleneck")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Drift fixes mild mutations", "When Ne s falls below about 1, weakly\ndeleterious alleles drift up and stay;\nthe realised load rises for a long time", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Inbreeding exposes and purges", "Homozygosity exposes recessive alleles;\nselection removes them, so masked load\nfalls, at the cost of a short-term rise", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Counts are not fitness", "Allele counts per genome depend on\nannotation, dominance and reference bias;\nfitness effects must be measured", fc=bs.GREY_LIGHT)
a3.text(-0.2, 1.04, "b", transform=a3.transAxes, fontsize=10, fontweight="bold", va="bottom")
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "c", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig10_2_load_bottleneck"))
