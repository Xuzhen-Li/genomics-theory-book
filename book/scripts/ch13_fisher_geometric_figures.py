"""Chapter 13 figures: the chance that a random mutation is beneficial in Fisher geometric model.

Usage: python -B ch13_fisher_geometric_figures.py OUTDIR
Monte Carlo, seed 20261126. A phenotype sits at distance d = 1 from the optimum in n dimensions. A mutation
moves it by a vector of length r in a uniformly random direction; it is beneficial if the new phenotype is
closer to the optimum. For each n (2, 10, 50) and each scaled size x = r * sqrt(n) / (2 d), 20000 random
mutations are drawn. The curve is Fisher large-n result P = 1 - Phi(x).
"""
import os, sys, math
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
xs = np.linspace(0.05, 2.5, 15)
res = {}
for n in (2, 10, 50):
    p = []
    for x in xs:
        r = 2 * x / math.sqrt(n)
        u = rng.normal(size=(20000, n))
        u /= np.linalg.norm(u, axis=1)[:, None]
        z = np.zeros(n); z[0] = 1.0
        newd = np.linalg.norm(z[None, :] + r * u, axis=1)
        p.append(np.mean(newd < 1.0))
        print("n=%d x=%.3f P(beneficial)=%.4f" % (n, x, p[-1]))
    res[n] = np.array(p)
xx = np.linspace(0, 2.6, 200)
theory = np.array([0.5 * math.erfc(v / math.sqrt(2)) for v in xx])
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
a1.plot(xx, theory, color="#000000", lw=1.2, label="Fisher: 1 - \u03a6(x)")
for (n, p), col, mk in zip(res.items(), (bs.ORANGE, bs.BLUE, bs.GREEN), ("s", "o", "^")):
    a1.plot(xs, p, ls="none", marker=mk, ms=3.5, color=col, label="simulated, n = %d traits" % n)
a1.set_xlim(0, 2.6); a1.set_ylim(-0.02, 0.62)
a1.set_xlabel("Scaled mutation size x = r\u221an / (2d)"); a1.set_ylabel("Probability the mutation is beneficial")
a1.legend(frameon=False, loc="upper right")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Small steps", "Almost half of very small mutations\nmove the phenotype closer to the\noptimum, whatever the number of traits", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Large steps and many traits", "The chance falls fast with size and\nwith n: the cost of complexity", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "What Fisher did not include", "Drift loses most small beneficial\nmutations, so the steps that fix are\nlarger than Fisher expected", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig13_2_fisher_geometric_model"))
