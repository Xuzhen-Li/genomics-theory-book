"""Shared style and layout checks for Genomics Theory Book figures.

Style follows a Nature-like house style: Liberation Sans, 6-10 pt text, no grid,
0.5 pt frames. check(fig) enforces: text >= 6 pt, contrast >= 4.5:1 against the
background behind it, every text inside the figure, text inside its panel with
padding, and annotation text not crossing an axes frame.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import to_rgb

BLUE, ORANGE, GREEN, RED, PURPLE = "#1F72AE", "#F77E12", "#119B76", "#CC312C", "#595594"
GREEN_TXT, ORANGE_TXT = "#0B6E52", "#A34F00"
GREY_TXT, GREY_BAND, GREY_LIGHT = "#6B6B6B", "#BFBFBF", "#F0F0F0"
BLUE_BG, RED_BG = "#DEE4F0", "#F6DEDE"
MM = 1 / 25.4


def setup():
    plt.rcParams.update({
        "font.family": ["Liberation Sans", "Noto Sans CJK SC"],
        "font.size": 7, "axes.titlesize": 8, "axes.labelsize": 8,
        "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "axes.linewidth": 0.5, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
        "xtick.major.size": 2.5, "ytick.major.size": 2.5, "axes.grid": False,
        "svg.fonttype": "none", "savefig.dpi": 300,
    })


def _lum(c):
    def ch(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = to_rgb(c)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted([_lum(a), _lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


_PANELS = []


def panel(ax, x, y, w, h, title, body="", fc="#FFFFFF", ec="#333333", tsize=8, bsize=7, tcolor="#000000"):
    """Rounded panel in axes-fraction coordinates with a title and body text."""
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012",
                       fc=fc, ec=ec, lw=0.6, transform=ax.transAxes)
    ax.add_patch(p)
    t1 = ax.text(x + 0.012, y + h - 0.015, title, ha="left", va="top", fontsize=tsize,
                 fontweight="bold", color=tcolor, transform=ax.transAxes)
    texts = [t1]
    if body:
        texts.append(ax.text(x + 0.012, y + h - 0.015 - tsize * 0.0062 - 0.02, body, ha="left", va="top",
                             fontsize=bsize, color="#000000", transform=ax.transAxes, linespacing=1.3))
    _PANELS.append((p, texts, fc))
    return p


def _offscale_tick(t, ax):
    try:
        x, y = t.get_position()
    except Exception:
        return False
    lo, hi = sorted(ax.get_xlim()) if t in ax.get_xticklabels() else sorted(ax.get_ylim())
    v = x if t in ax.get_xticklabels() else y
    return not (lo - 1e-9 <= v <= hi + 1e-9)


def check(fig):
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    fb = fig.bbox
    problems = []
    framed = {}
    for p, texts, fc in _PANELS:
        for t in texts:
            framed[id(t)] = (p, fc)
    for t in fig.findobj(matplotlib.text.Text):
        if not t.get_visible() or not t.get_text().strip():
            continue
        ax = t.axes
        if ax is not None and not ax.axison and t not in ax.texts:
            continue
        if ax is not None and (t in ax.get_xticklabels() or t in ax.get_yticklabels()) and _offscale_tick(t, ax):
            continue
        s = t.get_text().replace("\n", " ")[:30]
        if t.get_fontsize() < 6:
            problems.append("small font %.1f: %s" % (t.get_fontsize(), s))
        bg = framed.get(id(t), (None, "#FFFFFF"))[1]
        bbp = t.get_bbox_patch()
        if bbp is not None:
            bg = bbp.get_facecolor()[:3]
        if contrast(t.get_color(), bg) < 4.5:
            problems.append("low contrast %.2f: %s" % (contrast(t.get_color(), bg), s))
        e = t.get_window_extent(r)
        if e.x0 < fb.x0 + 2 or e.y0 < fb.y0 + 2 or e.x1 > fb.x1 - 2 or e.y1 > fb.y1 - 2:
            problems.append("outside figure: " + s)
        if id(t) in framed:
            pb = framed[id(t)][0].get_window_extent(r)
            if e.x0 < pb.x0 + 3 or e.x1 > pb.x1 - 3 or e.y0 < pb.y0 + 3 or e.y1 > pb.y1 - 3:
                problems.append("touches panel edge: " + s)
        elif ax is not None and t in ax.texts and ax.axison:
            ab = ax.get_window_extent(r)
            inside = e.x0 >= ab.x0 + 2 and e.x1 <= ab.x1 - 2 and e.y0 >= ab.y0 + 2 and e.y1 <= ab.y1 - 2
            outside = e.x1 <= ab.x0 or e.x0 >= ab.x1 or e.y1 <= ab.y0 or e.y0 >= ab.y1
            if not (inside or outside):
                problems.append("crosses axes frame: " + s)
    return problems


def save(fig, path_noext):
    probs = check(fig)
    if probs:
        raise SystemExit("figure check failed for %s:\n  %s" % (path_noext, "\n  ".join(probs)))
    fig.savefig(path_noext + ".png", dpi=300)
    fig.savefig(path_noext + ".svg")
    _PANELS.clear()
    print("saved", path_noext)
