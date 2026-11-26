"""Chapter 1 figures: Mendel’s laws and exceptions (schematic) and power of a 1:1 segregation test.

Usage: python -B ch01_mendel_figures.py OUTDIR
Seed 20261126. Needs numpy and matplotlib; bookstyle.py must be importable.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
rng = np.random.default_rng(20261126)

# Figure 1.2: schematic
fig = plt.figure(figsize=(183 * bs.MM, 100 * bs.MM))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off(); ax.set_xticks([]); ax.set_yticks([])
bs.panel(ax, 0.02, 0.77, 0.47, 0.20, "Law of segregation",
       "Aa gives A and a gametes 1:1\nF2 of Aa x Aa: 1 AA : 2 Aa : 1 aa\nTest cross Aa x aa: 1 Aa : 1 aa", fc=bs.BLUE_BG)
bs.panel(ax, 0.51, 0.77, 0.47, 0.20, "Law of independent assortment",
       "Unlinked loci A and B combine at random\nF2: 9 : 3 : 3 : 1\nTest cross: 1 : 1 : 1 : 1", fc=bs.BLUE_BG)
ax.text(0.5, 0.735, "Exceptions change the ratios, not the particulate gene", ha="center", va="top",
        fontsize=8, fontweight="bold", color="#000000")
items = [
    ("Linkage", "Loci on one chromosome co-segregate;\nrecombination fraction < 0.5\n(Morgan 1910; Sturtevant 1913)"),
    ("Segregation distortion", "Drive or killer-protector systems;\nrice S5 locus in indica x japonica\n(Sandler & Novitski 1957; Yang 2012)"),
    ("Parent-of-origin effects", "Expression depends on the parent\nthat transmitted the allele;\nmaize R-mottled (Kermicle 1970)"),
    ("Paramutation", "One allele changes the heritable\nstate of the other; maize b1, R\n(Brink 1956; Chandler 2007)"),
    ("Organelle inheritance", "Plastids and mitochondria sort out\nwithout Mendelian ratios\n(Baur; Hagemann 2000)"),
    ("Polysomic segregation", "Autotetraploid AAaa gametes\nAA : Aa : aa = 1 : 4 : 1, plus\ndouble reduction (Haldane 1930)"),
]
w, h = 0.3, 0.30
for i, (t, b) in enumerate(items):
    c, r = i % 3, i // 3
    bs.panel(ax, 0.02 + c * (w + 0.03), 0.355 - r * (h + 0.03), w, h, t, b, fc=bs.GREY_LIGHT)
bs.save(fig, os.path.join(out, "fig01_2_mendel_exceptions_schematic"))

# Figure 1.3: power simulation
sizes = np.array([25, 50, 100, 200, 400, 800, 1600])
runs = 20000
def power(k, n):
    x = rng.binomial(n, k, size=runs)
    chi = (x - n / 2) ** 2 / (n / 4)  # 1:1 chi-square, 1 df
    return np.mean(chi > 3.841)
fig, ax = plt.subplots(figsize=(89 * bs.MM, 70 * bs.MM))
fig.subplots_adjust(left=0.16, right=0.97, bottom=0.17, top=0.95)
styles = [(0.55, bs.BLUE, bs.BLUE), (0.60, bs.ORANGE, bs.ORANGE_TXT), (0.70, bs.RED, bs.RED)]
for k, col, tcol in styles:
    p = [power(k, n) for n in sizes]
    ax.plot(sizes, p, "-o", color=col, lw=1.4, ms=3.5, mec="#333333", mew=0.3)
    j = 3 if k == 0.55 else (1 if k == 0.60 else 0)
    dy = -0.07 if k == 0.55 else 0
    ax.text(sizes[j] * 1.12, p[j] + dy, "k = %.2f" % k, color=tcol, fontsize=7, va="center", ha="left")
p0 = [power(0.5, n) for n in sizes]
ax.plot(sizes, p0, "--", color=bs.GREY_TXT, lw=1.0)
ax.text(400, 0.11, "k = 0.50 (false positives)", color=bs.GREY_TXT, fontsize=7, ha="center")
ax.axhline(0.8, color=bs.GREY_BAND, lw=0.6, zorder=0)
ax.text(1550, 0.745, "power 0.8", color=bs.GREY_TXT, fontsize=7, ha="right")
ax.set_xscale("log"); ax.set_xticks(sizes); ax.set_xticklabels([str(s) for s in sizes])
ax.minorticks_off()
ax.set_xlim(20, 2000); ax.set_ylim(0, 1.05); ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_xlabel("Progeny per family"); ax.set_ylabel("Share of tests with P < 0.05")
bs.save(fig, os.path.join(out, "fig01_3_segregation_power_sim"))
