"""Appendix A figure: which status labels each chapter of the book uses.

Usage: python -B appA_status_figures.py OUTDIR [STATUS.md]
Reads the status table in book/STATUS.md (by default the file one level above this script) and marks, for
each chapter, whether its status cell uses the labels Verified, Partly verified, Contested and Rejected.
"Verified" is counted only outside the phrase "Partly verified". The result is deterministic for a given
STATUS.md; rerun the script after the table changes.
"""
import os, re, sys
import matplotlib.pyplot as plt
import bookstyle as bs

out = sys.argv[1]
src = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "STATUS.md")
os.makedirs(out, exist_ok=True)
bs.setup()
LABELS = ["Verified", "Partly verified", "Contested", "Rejected"]
COLS = [bs.GREEN, bs.BLUE, bs.ORANGE, bs.RED]
rows = []
for line in open(src, encoding="utf-8"):
    c = [x.strip() for x in line.split("|")]
    if len(c) > 4 and re.fullmatch(r"\d\d", c[1]):
        s = c[3]
        rest = s.replace("Partly verified", "")
        rows.append((int(c[1]), ["Verified" in rest, "Partly verified" in s, "Contested" in s, "Rejected" in s]))
rows.sort()
n = len(rows)
counts = [sum(r[1][j] for r in rows) for j in range(4)]
for ch, flags in rows:
    print("%02d %s" % (ch, ", ".join(l for l, f in zip(LABELS, flags) if f) or "none"))
print("chapters %d; counts %s" % (n, ", ".join("%s %d" % (l, k) for l, k in zip(LABELS, counts))))
fig = plt.figure(figsize=(160 * bs.MM, 110 * bs.MM))
a1 = fig.add_axes([0.09, 0.17, 0.42, 0.75])
a2 = fig.add_axes([0.66, 0.17, 0.30, 0.75])
for i, (ch, flags) in enumerate(rows):
    for j, f in enumerate(flags):
        if f:
            a1.scatter([j], [i], s=22, color=COLS[j], zorder=3)
        else:
            a1.scatter([j], [i], s=6, color=bs.GREY_BAND, zorder=2)
a1.set_xlim(-0.6, 3.6); a1.set_ylim(n - 0.4, -0.6)
a1.set_xticks(range(4)); a1.set_xticklabels(LABELS, rotation=30, ha="right")
a1.set_yticks(range(n)); a1.set_yticklabels(["%02d" % r[0] for r in rows], fontsize=6)
a1.set_ylabel("Chapter")
a1.tick_params(axis="x", length=0)
a2.barh(range(4), counts, color=COLS, height=0.6)
for j, k in enumerate(counts):
    a2.text(k + 0.4, j, str(k), va="center", fontsize=7)
a2.set_yticks(range(4)); a2.set_yticklabels(LABELS)
a2.set_ylim(3.6, -0.6); a2.set_xlim(0, 30)
a2.set_xticks([0, 10, 20, 30])
a2.set_xlabel("Chapters using the label")
a1.text(-0.2, 1.02, "a", transform=a1.transAxes, fontsize=10, fontweight="bold", va="bottom")
a2.text(-0.55, 1.02, "b", transform=a2.transAxes, fontsize=10, fontweight="bold", va="bottom")
bs.save(fig, os.path.join(out, "figA_1_status_overview"))
