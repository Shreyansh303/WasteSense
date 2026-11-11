"""Fig. 1 of the paper: the experimental pipeline shared by both generations.

    python paper/figures/scripts/m_pipeline.py      # -> paper/figures/m_pipeline.png

A plain block diagram. It is drawn at its printed size (one IEEE column, 3.5 in wide) and all coordinates are
in points, so the font size below is the size in print.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "m_pipeline.png"

plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "STIXGeneral", "DejaVu Serif"]})
PT = 8.0                       # text size in print
W, H = 252.0, 210.0            # one column wide
BOX_H, GAP = 30.0, 16.0        # box height and vertical gap between rows

fig = plt.figure(figsize=(W / 72, H / 72))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")


def box(x0, x1, top, text, height=BOX_H):
    ax.add_patch(Rectangle((x0, top - height), x1 - x0, height, linewidth=0.8, edgecolor="black", facecolor="white"))
    ax.text((x0 + x1) / 2, top - height / 2, text, ha="center", va="center", fontsize=PT, linespacing=1.15)
    return top - height


def arrow(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", linewidth=0.8, color="black", shrinkA=0, shrinkB=0,
                                mutation_scale=7))


L, R = 2.0, W - 2.0
ARM_W = (R - L - 2 * 8.0) / 3
A0, B0, C0 = L, L + ARM_W + 8.0, L + 2 * (ARM_W + 8.0)
XA, XB, XC = A0 + ARM_W / 2, B0 + ARM_W / 2, C0 + ARM_W / 2

# Row 1: data
top = H - 2.0
y = box(40, W - 40, top, "Training and validation data\n(Generation 1 or Generation 2)")
bar = y - GAP / 2
ax.plot([W / 2, W / 2], [y, bar], color="black", linewidth=0.8)
ax.plot([XA, XC], [bar, bar], color="black", linewidth=0.8)

# Row 2: the three arms
top = y - GAP
for x in (XA, XB, XC):
    arrow(x, bar, x, top)
box(A0, A0 + ARM_W, top, "Arm A\ndefault settings")
box(B0, B0 + ARM_W, top, "Arm B\nrandom search")
y = box(C0, C0 + ARM_W, top, "Arm C\nPSO")

# Row 3: proxy training, used by B and C only
top = y - GAP
arrow(XB, y, XB, top)
arrow(XC, y, XC, top)
y3 = box(B0, R, top, "32 proxy trainings each\n(12 epochs, 40% of the data)")

# Row 4: full training
top = y3 - GAP
arrow(XA, y, XA, top)
arrow((B0 + R) / 2, y3, (B0 + R) / 2, top)
ax.text((B0 + R) / 2 + 4, y3 - GAP / 2, "best setting", ha="left", va="center", fontsize=PT - 1, style="italic")
y = box(L, R, top, "Full training, 100 epochs (one run per arm)", height=22)

# Row 5: test
top = y - GAP
arrow(W / 2, y, W / 2, top)
box(L, R, top, "Test set, scored once\nmAP with bootstrap 95% confidence intervals")

fig.savefig(OUT, dpi=400)
print(f"Wrote {OUT} ({W:.0f} x {H:.0f} pt)")
