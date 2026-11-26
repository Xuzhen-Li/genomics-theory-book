"""Chapter 17 figures: a transposable element invading a sexual and an asexual population.

Usage: python -B ch17_selfish_dna_figures.py OUTDIR
Individual-based simulation, seed 20261126. N = 1000 diploid hosts, 1000 generations, five replicate runs per
mating system. Each host carries n copies of one element family at unlinked sites. Each generation: copies
transpose (Poisson, mean u n, u = 0.02) and are excised (binomial, v = 0.002); host fitness is
w(n) = exp(-a n - b n^2 / 2) with a = 0.003 and b = 0.0005 (synergistic harm); parents are drawn in proportion
to w. Sexual hosts: each parent passes each of its copies with probability 1/2. Asexual hosts: the offspring
copies the parent. At the start 5% of hosts carry 2 copies. The deterministic equilibrium for the sexual case is
n* = (u - v - a) / b = 30 copies per diploid genome.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
N, G, U, V, A, B = 1000, 1000, 0.02, 0.002, 0.003, 0.0005
NSTAR = (U - V - A) / B
def run(sexual):
    n = np.zeros(N, dtype=np.int64)
    n[: N // 20] = 2
    mean = [n.mean()]
    for g in range(G):
        w = np.exp(-A * n - B * n * n / 2.0)
        p = w / w.sum()
        if sexual:
            m = rng.choice(N, size=N, p=p); f = rng.choice(N, size=N, p=p)
            n = rng.binomial(n[m], 0.5) + rng.binomial(n[f], 0.5)
        else:
            n = n[rng.choice(N, size=N, p=p)]
        n = n + rng.poisson(U * n) - rng.binomial(n, V)
        mean.append(n.mean())
    return np.array(mean)
sex = [run(True) for _ in range(5)]
asex = [run(False) for _ in range(5)]
for i, (s, a) in enumerate(zip(sex, asex)):
    print("rep %d sexual end mean %.1f, asexual end mean %.2f" % (i, s[-1], a[-1]))
gen = np.arange(G + 1)
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for i, s in enumerate(sex):
    a1.plot(gen, s, color=bs.BLUE, lw=0.9, label="sexual hosts (5 runs)" if i == 0 else None)
for i, a in enumerate(asex):
    a1.plot(gen, a, color=bs.ORANGE, lw=1.6, zorder=3, label="asexual hosts (5 runs)" if i == 0 else None)
a1.axhline(NSTAR, color=bs.GREY_TXT, lw=0.8, ls=":", label="approximate equilibrium n* = 30")
a1.set_xlim(0, G); a1.set_ylim(-1, 50)
a1.set_xlabel("Generation"); a1.set_ylabel("Mean copies per host genome")
a1.legend(frameon=False, loc="upper left", fontsize=6.5)
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Spread despite harm", "With sex, copies move into new\ngenomes each generation and the\nelement spreads although it lowers fitness", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Copy number settles", "Synergistic harm stops the spread where\nnew copies balance selection and\nexcision: n* = (u - v - a) / b", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Trapped without sex", "In clones each element stays in its\nfirst host line, which selection removes", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig17_2_element_invasion"))
