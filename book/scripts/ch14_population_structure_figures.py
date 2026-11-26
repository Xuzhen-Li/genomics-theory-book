"""Chapter 14 figures: isolation by distance in a stepping-stone model compared with the island model.

Usage: python -B ch14_population_structure_figures.py OUTDIR
Exact equilibrium calculation, no random numbers. 2000 demes of N = 50 diploids (2N = 100 gene copies) on a
ring, large enough that the ring closure does not matter for the distances shown. Stepping-stone: each deme sends m/2 = 0.05 of its gene copies to each neighbour, so the axial
dispersal variance is sigma^2 = 0.1 steps^2 per generation. Island: the same total m = 0.1 comes from the
pool of all demes. F[i, j] is the probability that two gene copies from demes i and j are identical by
descent. Each generation F = (1 - u)^2 * W (F + diag((1 - F_kk) / 2N)) W^T (Malecot recursion). Both
migration matrices are circulant, so the equilibrium is solved exactly in Fourier space. Pairwise FST = (Fw - Fb) / (1 - Fb), with Fw
the identity within a deme and Fb between the two demes. Rousset (1997) predicts that FST/(1 - FST) grows
linearly with distance r in one dimension, with slope 1/(4 D sigma^2) = 1/(4 * 50 * 0.1) = 0.05 here, while
distances stay well below the mutation scale sigma / sqrt(2u).
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
D, N2, M = 2000, 100, 0.1
k = np.arange(D)
lam_s = 1 - M + M * np.cos(2 * np.pi * k / D)
lam_i = np.where(k == 0, 1.0, 1 - M)
def curve(lam, u):
    c = (1 - u) ** 2
    h = c * lam ** 2 / (1 - c * lam ** 2) / N2
    g = h.mean()
    f0 = g / (1 + g)
    Fhat = h * (1 - f0)
    F = np.real(np.fft.ifft(Fhat))
    r = np.arange(1, 21)
    fst = (F[0] - F[r]) / (1 - F[r])
    return r, fst / (1 - fst)
res = []
for lab, W, u, col, mk in (("stepping-stone, u = 1e-6", lam_s, 1e-6, bs.BLUE, "o"),
                           ("stepping-stone, u = 5e-4", lam_s, 5e-4, bs.GREEN, "^"),
                           ("island model, u = 1e-6", lam_i, 1e-6, bs.ORANGE, "s")):
    r, y = curve(W, u)
    res.append((lab, r, y, col, mk))
    sl = np.polyfit(r, y, 1)
    print(lab, "slope %.4f intercept %.4f" % (sl[0], sl[1]), " ".join("%.3f" % v for v in y))
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for lab, r, y, col, mk in res:
    a1.plot(r, y, color=col, lw=1.0, marker=mk, ms=3.2, label=lab)
a1.plot([0, 20], [res[0][2][0] - 0.05, res[0][2][0] - 0.05 + 0.05 * 20], color=bs.GREY_TXT, lw=0.8, ls=":", label="slope 1/(4D\u03c3\u00b2) = 0.05")
a1.set_xlim(0, 21); a1.set_ylim(0, 1.25)
a1.set_xlabel("Distance between demes (steps)"); a1.set_ylabel("FST / (1 - FST)")
a1.legend(frameon=False, loc="upper left")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Isolation by distance", "With local dispersal, differentiation\ngrows with distance; in one dimension\nFST/(1 - FST) rises linearly", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Island model", "Migrants come from anywhere, so all\npairs are equally different and the\nline is flat", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Reading the slope", "Slope 1/(4D\u03c3\u00b2) in one dimension and\n1/(4\u03c0D\u03c3\u00b2) against log distance in two;\nit bends at distances near \u03c3/\u221a(2u)", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig14_2_isolation_by_distance"))
