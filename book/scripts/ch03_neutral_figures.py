"""Chapter 3 figures: neutral substitution rate vs population size (Wright-Fisher), and the MK table.

Usage: python -B ch03_neutral_figures.py OUTDIR
Seed 20261126. Haploid Wright-Fisher, infinite sites, mutation rate 0.02 per genome per generation.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
MU, GENS, BURN = 0.02, 40000, 4000

def run(N):
    freqs = np.zeros(0, dtype=np.int64)
    fixed = 0; seg = []
    for g in range(GENS):
        if freqs.size:
            freqs = rng.binomial(N, freqs / N)
        new = rng.poisson(N * MU)
        if new:
            freqs = np.concatenate([freqs, np.ones(new, dtype=np.int64)])
        if g >= BURN:
            fixed += int(np.sum(freqs == N))
            seg.append(int(np.sum((freqs > 0) & (freqs < N))))
        freqs = freqs[(freqs > 0) & (freqs < N)]
    return fixed / (GENS - BURN), float(np.mean(seg))

Ns = [10, 20, 40, 80, 160]
rates, segs = zip(*[run(N) for N in Ns])
for N, r, s in zip(Ns, rates, segs):
    print("N=%d substitution rate=%.4f mean segregating=%.1f" % (N, r, s))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(150 * bs.MM, 62 * bs.MM))
fig.subplots_adjust(left=0.10, right=0.98, bottom=0.2, top=0.88, wspace=0.38)
a1.plot(Ns, rates, "-o", color=bs.BLUE, lw=1.4, ms=3.5, mec="#333333", mew=0.3)
a1.axhline(MU, color=bs.GREY_TXT, lw=0.8, ls="--")
a1.text(160, MU * 1.12, "mutation rate 0.02", color=bs.GREY_TXT, ha="right", fontsize=7)
a1.set_xscale("log"); a1.set_xticks(Ns); a1.set_xticklabels([str(n) for n in Ns]); a1.minorticks_off()
a1.set_xlim(8, 200); a1.set_ylim(0, 0.03); a1.set_yticks([0, 0.01, 0.02, 0.03])
a1.set_xlabel("Population size N"); a1.set_ylabel("Substitutions per generation")
a2.plot(Ns, segs, "-o", color=bs.RED, lw=1.4, ms=3.5, mec="#333333", mew=0.3)
a2.set_xscale("log"); a2.set_yscale("log"); a2.set_xticks(Ns); a2.set_xticklabels([str(n) for n in Ns]); a2.minorticks_off()
a2.set_xlim(8, 200); a2.set_ylim(1, 150); a2.set_yticks([1, 3, 10, 30, 100]); a2.set_yticklabels(["1", "3", "10", "30", "100"])
a2.set_xlabel("Population size N"); a2.set_ylabel("Mean segregating sites")
for a, l in ((a1, "a"), (a2, "b")):
    a.text(-0.24, 1.04, l, transform=a.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig03_2_neutral_rate_sim"))

# Figure 3.3: MK table
fig = plt.figure(figsize=(150 * bs.MM, 70 * bs.MM))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off(); ax.set_xticks([]); ax.set_yticks([])
bs.panel(ax, 0.03, 0.08, 0.50, 0.86, "McDonald-Kreitman table", fc=bs.GREY_LIGHT)
for (x, y, t, w) in [(0.30, 0.74, "Fixed between\nspecies (D)", "bold"), (0.44, 0.74, "Polymorphic\nwithin (P)", "bold"),
                     (0.06, 0.55, "Nonsynonymous", "bold"), (0.30, 0.55, "Dn", "normal"), (0.44, 0.55, "Pn", "normal"),
                     (0.06, 0.38, "Synonymous", "bold"), (0.30, 0.38, "Ds", "normal"), (0.44, 0.38, "Ps", "normal")]:
    ax.text(x, y, t, ha="left" if x < 0.2 else "center", va="center", fontsize=7.5, fontweight=w, transform=ax.transAxes)
ax.plot([0.05, 0.51], [0.465, 0.465], color="#333333", lw=0.5, transform=ax.transAxes)
ax.plot([0.05, 0.51], [0.645, 0.645], color="#333333", lw=0.5, transform=ax.transAxes)
ax.text(0.06, 0.18, "Neutral expectation: Dn / Ds = Pn / Ps", ha="left", va="center", fontsize=7.5, transform=ax.transAxes)
bs.panel(ax, 0.56, 0.52, 0.41, 0.42, "Adaptive proportion",
       "alpha = 1 - (Ds x Pn) / (Dn x Ps)\n\nalpha > 0: excess nonsynonymous\nfixed differences", fc=bs.BLUE_BG)
bs.panel(ax, 0.56, 0.08, 0.41, 0.38, "Bias to correct",
       "Slightly deleterious polymorphisms\ninflate Pn and push alpha down;\nfit the DFE or drop rare variants", fc=bs.RED_BG)
bs.save(fig, os.path.join(out, "fig03_3_mk_test_schematic"))
