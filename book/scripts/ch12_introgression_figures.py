"""Chapter 12 figures: the D statistic (ABBA-BABA) under incomplete lineage sorting and introgression.

Usage: python -B ch12_introgression_figures.py OUTDIR
Coalescent simulation, seed 20261126, one haploid lineage from each of P1, P2, P3 and an outgroup O, all
populations of equal size, time in units of 2N generations. Tree ((P1,P2),P3),O with splits at 0.5 (P1-P2),
1.0 (P12-P3) and 3.0 (O). At time tm a lineage in P2 moves to P3 with probability f (gene flow from P3 into P2,
looking forwards). Under infinite sites the expected ABBA count is proportional to the length of the branch
ancestral to P2 and P3 only, and BABA to the branch ancestral to P1 and P3 only, so D is computed from summed
branch lengths over 50000 independent loci per value of f.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)
T12, T123, TO = 0.5, 1.0, 3.0
def locus(f, tm):
    pop = {frozenset("a"): "1", frozenset("b"): "2", frozenset("c"): "3", frozenset("o"): "O"}
    born = {k: 0.0 for k in pop}
    lens = {"bc": 0.0, "ac": 0.0}
    events = [(tm, "mig"), (T12, "m12"), (T123, "m123"), (TO, "mall"), (np.inf, "end")]
    t = 0.0
    for te, ev in events:
        while True:
            groups = {}
            for k, p in pop.items():
                groups.setdefault(p, []).append(k)
            rates = {p: len(v) * (len(v) - 1) / 2 for p, v in groups.items()}
            tot = sum(rates.values())
            if tot == 0:
                break
            dt = rng.exponential(1 / tot)
            if t + dt >= te:
                break
            t += dt
            ps = list(rates); pr = np.array([rates[p] for p in ps]) / tot
            p = ps[rng.choice(len(ps), p=pr)]
            i, j = rng.choice(len(groups[p]), 2, replace=False)
            x, y = groups[p][i], groups[p][j]
            for n in (x, y):
                if n == frozenset("bc"):
                    lens["bc"] += t - born[n]
                if n == frozenset("ac"):
                    lens["ac"] += t - born[n]
                del pop[n]
            z = x | y; pop[z] = p; born[z] = t
            if len(pop) == 1:
                return lens
        t = te
        if ev == "mig":
            for k in pop:
                if pop[k] == "2" and rng.random() < f:
                    pop[k] = "3"
        elif ev == "m12":
            for k in pop:
                if pop[k] in ("1", "2"):
                    pop[k] = "12"
        elif ev == "m123":
            for k in pop:
                if pop[k] in ("12", "3"):
                    pop[k] = "123"
        elif ev == "mall":
            for k in pop:
                pop[k] = "all"
    return lens
fs = np.arange(7) * 0.05
res = {}
for tm, lab in [(0.1, "recent gene flow (tm = 0.1)"), (0.4, "older gene flow (tm = 0.4)")]:
    D = []
    for f in fs:
        bc = ac = 0.0
        for r in range(50000):
            L = locus(f, tm); bc += L["bc"]; ac += L["ac"]
        D.append((bc - ac) / (bc + ac))
        print("tm=%.1f f=%.2f ABBA %.1f BABA %.1f D %.3f" % (tm, f, bc, ac, D[-1]))
    res[lab] = np.array(D)
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for (lab, D), col, mk in zip(res.items(), (bs.BLUE, bs.ORANGE), ("o", "s")):
    a1.plot(fs, D, color=col, lw=1.3, marker=mk, ms=3.5, label=lab)
a1.axhline(0, color=bs.GREY_TXT, lw=0.6, ls=":")
a1.set_xlim(-0.01, 0.31); a1.set_ylim(-0.1, 0.75); a1.set_yticks([0, 0.2, 0.4])
a1.set_xlabel("Fraction of P2 lineages from P3 (f)"); a1.set_ylabel("D = (ABBA - BABA) / (ABBA + BABA)")
a1.legend(frameon=False, loc="upper left")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Incomplete lineage sorting", "Discordant gene trees ABBA and BABA\nare equally common without gene flow,\nso D is near zero", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Introgression P3 into P2", "Adds ABBA trees only; D rises with f,\nbut its value is not the admixture\nproportion (use f statistics for that)", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Other causes of D > 0", "Ancestral population structure,\nunequal rates, sequencing error and\ngene flow from unsampled lineages", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig12_2_d_statistic"))
