"""Chapter 8 figures: expected diversity under background selection versus local recombination rate,
and how the linked selection processes differ.

Usage: python -B ch08_linked_selection_figures.py OUTDIR
No random numbers. Neutral site in the middle of a 2 Mb region with deleterious mutations spread
evenly (rate u per bp), selection against heterozygotes sh, recombination c per bp (no interference).
Integrating the standard single-site background selection term over the region gives
B = exp(-U / (sh + R (1 - sh))), with U = 2 L u and R = c L, L = 1 Mb on each side.
This ignores interference among selected sites, which matters when Ne s is small.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
bs.setup()
L = 1e6
cm = np.logspace(-2, 1, 300)
c = cm * 1e-8
cases = [("sh = 0.01, u = 5e-9 per bp", 0.01, 5e-9, bs.BLUE, "-"),
         ("sh = 0.001, u = 5e-9 per bp", 0.001, 5e-9, bs.ORANGE, "-"),
         ("sh = 0.01, gene-dense, u = 1e-8", 0.01, 1e-8, bs.PURPLE, "--")]
fig = plt.figure(figsize=(160 * bs.MM, 66 * bs.MM))
a1 = fig.add_axes([0.10, 0.2, 0.44, 0.68])
a2 = fig.add_axes([0, 0, 1, 1])
for lab, sh, u, col, ls in cases:
    B = np.exp(-(2 * L * u) / (sh + c * L * (1 - sh)))
    a1.plot(cm, B, color=col, lw=1.4, ls=ls, label=lab)
    print("%s: B at 0.1 cM/Mb %.3f, at 1 cM/Mb %.3f" % (lab, np.interp(0.1, cm, B), np.interp(1, cm, B)))
a1.set_xscale("log"); a1.minorticks_off()
a1.set_xlim(0.01, 10); a1.set_xticks([0.01, 0.1, 1, 10]); a1.set_xticklabels(["0.01", "0.1", "1", "10"])
a1.set_ylim(0, 1.3); a1.set_yticks([0, 0.25, 0.5, 0.75, 1])
a1.set_xlabel("Local recombination rate (cM/Mb)"); a1.set_ylabel("Expected diversity / neutral (B)")
a1.legend(frameon=False, loc="upper left")
a2.set_axis_off(); a2.set_xticks([]); a2.set_yticks([])
bs.panel(a2, 0.585, 0.62, 0.40, 0.27, "Background selection", "Steady loss near selected sites; mild\nSFS skew; strongest in gene-dense,\nlow-recombination regions", fc=bs.BLUE_BG)
bs.panel(a2, 0.585, 0.32, 0.40, 0.27, "Recurrent sweeps (hitchhiking)", "Troughs around adaptive fixations;\nexcess high-frequency derived alleles;\nlong shared haplotypes", fc=bs.RED_BG)
bs.panel(a2, 0.585, 0.02, 0.40, 0.27, "Shared signal, so not decisive", "Both lower diversity where recombination\nis low; separate them with SFS, haplotype\nand divergence data", fc=bs.GREY_LIGHT)
a1.text(-0.2, 1.04, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(0.575, 0.90, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "fig08_2_background_selection"))
