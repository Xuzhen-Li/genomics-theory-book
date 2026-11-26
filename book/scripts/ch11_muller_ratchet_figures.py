"""Chapter 11 figures: Muller ratchet clicks in asexual populations of different size.

Usage: python -B ch11_muller_ratchet_figures.py OUTDIR
Wright-Fisher simulation of a haploid asexual population, seed 20261126. Each individual carries k deleterious
mutations with multiplicative fitness (1 - s)^k; parents are drawn with probability proportional to fitness and
each offspring gains a Poisson(U) number of new mutations. U = 0.1, s = 0.02, so the deterministic least-loaded
class has size n0 = N exp(-U/s) (Haigh 1978). Start from the mutation-selection balance, Poisson(U/s).
The minimum k in the population is recorded; each increase is one click of the ratchet.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
U, s, G = 0.1, 0.02, 3000
res = {}
for N in (100, 1000, 10000):
    k = rng.poisson(U / s, N)
    mins = []
    for g in range(G):
        mins.append(k.min())
        w = (1 - s) ** (k - k.min())
        par = rng.choice(N, size=N, p=w / w.sum())
        k = k[par] + rng.poisson(U, N)
    res[N] = np.array(mins) - mins[0]
    print("N=%d n0=%.2f clicks in %d generations: %d" % (N, N * np.exp(-U / s), G, res[N][-1]))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for N, col, ls in [(100, bs.RED, "-"), (1000, bs.ORANGE, "--"), (10000, bs.BLUE, "-")]:
    a1.step(np.arange(G), res[N], where="post", color=col, lw=1.3, ls=ls, label="N = %d (n0 = %.1f)" % (N, N * np.exp(-U / s)))
a1.set_xlim(0, G); a1.set_ylim(0, 1.45 * max(r.max() for r in res.values()))
a1.set_xlabel("Generation"); a1.set_ylabel("Clicks (rise in fewest mutations carried)")
a1.legend(frameon=False, loc="upper left")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "The ratchet", "Without recombination the least-loaded\nclass, once lost by drift, cannot be\nrebuilt except by back mutation", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Speed set by n0 = N exp(-U/s)", "Small n0 gives frequent clicks; a large\npopulation or strong selection slows it;\nfalling fitness can lead to meltdown", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "What stops it", "Recombination, rare sex, gene\nconversion, back or compensatory\nmutation, and selection among lineages", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig11_2_muller_ratchet"))
