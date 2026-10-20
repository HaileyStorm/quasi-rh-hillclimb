"""Timeline of the best quasi-RH boundary, from OpenAI's 7/8 preprint to the current
QuasiRiemannTracker record, plus this repo's conditional nested-level results.
Writes graphs/timeline.png and graphs/timeline.csv.

Sources: the tracker's submissions/*/metadata.json and its admission-records branch
(theta_exact and first verification time of each admitted record). Only records that
improved on the best bound at the time are plotted. Every point is labeled with its
contributor; the crowded Oct 13-20 stretch is labeled in a column with leader lines.
"""
import csv
import os
from datetime import datetime
from fractions import Fraction as Fr

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0"
BLUE, ORANGE, ORANGE_TEXT = "#2a78d6", "#eb6834", "#b5461a"   # validated pair; darker orange for text
plt.rcParams.update({"font.family": ["Inter", "DejaVu Sans"], "font.size": 11,
                     "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})

# (time UTC, contributor, theta, short theta label)
RECORDS = [
    ("2026-09-30 12:00", "OpenAI (preprint)", Fr(7, 8), "7/8"),
    ("2026-10-08 00:00", "Argonaut Math", Fr(3499999, 4000000), "0.87499975"),
    ("2026-10-08 16:18", "Baiying Liu", Fr(874957069799168740018340006959, 10**30), "0.8749571"),
    ("2026-10-09 11:37", "Tim Gehrunger / ProofCouncil", Fr(874957019421, 10**12), "0.8749570"),
    ("2026-10-10 13:35", "Akash Levy", Fr(10499, 12000), "10499/12000"),
    ("2026-10-10 16:09", "Hailey Collet", Fr(683505193, 781250000), "0.8748866"),
    ("2026-10-13 06:44", "nielstron", Fr(87487, 100000), "0.87487"),
    ("2026-10-13 13:04", "Kari Roegnvaldsson", Fr(4374347, 5000000), "0.8748694"),
    ("2026-10-13 14:41", "Kari Roegnvaldsson", Fr(87486797, 10**8), "0.87486797"),
    ("2026-10-13 18:43", "Hailey Collet", Fr(874861, 10**6), "0.874861"),
    ("2026-10-14 10:07", "Zhongpai Gao", Fr(4374299, 5000000), "0.8748598"),
    ("2026-10-14 22:53", "timbalud", Fr(8748559, 10**7), "0.8748559"),
    ("2026-10-15 03:53", "DaysSky", Fr(437423, 500000), "0.874846"),
    ("2026-10-15 05:29", "Zhongpai Gao", Fr(21871, 25000), "0.87484"),
    ("2026-10-16 16:03", "Zhongpai Gao", Fr(218709, 250000), "0.874836"),
    ("2026-10-17 11:32", "Zhongpai Gao", Fr(87483, 100000), "0.87483"),
    ("2026-10-20 00:51", "Sil", Fr(874828524351, 10**12), "0.8748285"),
    ("2026-10-20 01:49", "ArviFoxy (current record)", Fr(174963413, 200000000), "0.874817065"),
]
CONDITIONAL = [
    ("2026-10-20 15:00", "rohanarun · 3 levels (conditional)", Fr(874812431, 10**9), "≤ 0.874812431  (−4.6·10⁻⁶)"),
    ("2026-10-20 21:00", "rohanarun · 4 levels (conditional)", Fr(437405141, 500000000), "≤ 0.874810282  (−6.8·10⁻⁶)"),
]


def ts(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


t = [ts(r[0]) for r in RECORDS]
y = [float(r[2]) for r in RECORDS]
tc = [ts(r[0]) for r in CONDITIONAL]
yc = [float(r[2]) for r in CONDITIONAL]

fig = plt.figure(figsize=(14, 7.4), facecolor=SURF)
fig.text(0.05, 0.945, "Quasi-RH: the zero-free boundary θ over time", fontsize=17, weight="bold")
fig.text(0.05, 0.905, "Best all-moduli Dirichlet boundary (zero-free for Re s > θ). Lower is better. "
         "Blue: Lean-verified records. Orange: conditional, not Lean-verified (gain vs current record in brackets).", fontsize=11, color=INK2)
ax = fig.add_axes([0.08, 0.12, 0.90, 0.74], facecolor=SURF)

ax.step(t + [tc[-1]], y + [y[-1]], where="post", color=BLUE, lw=2, zorder=2)
ax.scatter(t, y, s=46, color=BLUE, edgecolor=SURF, linewidth=2, zorder=3)
ax.plot([t[-1]] + tc, [y[-1]] + yc, color=ORANGE, lw=2, ls=(0, (3, 3)), zorder=2)
ax.scatter(tc, yc, s=70, facecolor=SURF, edgecolor=ORANGE, linewidth=2.2, zorder=4)

# early records: labels beside the points (offsets in points)
EARLY = {0: (10, -16, "left"), 1: (-12, 14, "right"), 2: (-12, 0, "right"),
         3: (12, 14, "left"), 4: (-12, 0, "right"), 5: (-12, -12, "right")}
for i, (dx, dy, ha) in EARLY.items():
    ax.annotate(f"{RECORDS[i][1]}  {RECORDS[i][3]}", (t[i], y[i]), xytext=(dx, dy),
                textcoords="offset points", ha=ha, va="center", fontsize=9.5, color=INK,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.7, shrinkA=0, shrinkB=4))

# crowded stretch and conditional points: a label column on the right, with leader lines
late = [(t[i], y[i], f"{RECORDS[i][1]}  {RECORDS[i][3]}", False) for i in range(6, len(RECORDS))]
late += [(tc[k], yc[k], f"{CONDITIONAL[k][1]}  {CONDITIONAL[k][3]}", True) for k in range(len(CONDITIONAL))]
col_x = datetime(2026, 10, 22, 6)
top, bottom = 0.874895, 0.874795
step = (top - bottom) / (len(late) - 1)
for k, (tx, yy, label, cond) in enumerate(late):
    ax.annotate(label, (tx, yy), xytext=(col_x, top - k * step), textcoords="data", ha="left", va="center",
                fontsize=9.5, color=ORANGE_TEXT if cond else INK, weight="bold" if cond else "normal",
                arrowprops=dict(arrowstyle="-", color=ORANGE if cond else MUTED, lw=0.7, shrinkA=3, shrinkB=4,
                                relpos=(0, 0.5)))

ax.set_ylim(0.87478, 0.875025)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.5f"))
ax.set_xlim(datetime(2026, 9, 29), datetime(2026, 11, 1))
ax.set_xticks([datetime(2026, 9, 30)] + [datetime(2026, 10, d) for d in (3, 6, 9, 12, 15, 18, 21)])
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
for s in ("left", "right", "top"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color(GRID)
ax.tick_params(length=0)
ax.set_ylabel("θ")

fig.text(0.05, 0.02, "Sources: QuasiRiemannTracker submissions and admission records (first verification times); "
         "OpenAI preprint dated Sep 30, 2026.\n"
         "Only bounds that beat the record at the time are shown. Conditional results: "
         "github.com/rohanarun/quasi-rh-hillclimb (depth3/PROOF.md)", fontsize=8.5, color=MUTED)

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "graphs")
os.makedirs(out_dir, exist_ok=True)
fig.savefig(os.path.join(out_dir, "timeline.png"), dpi=200, facecolor=SURF)
with open(os.path.join(out_dir, "timeline.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["time_utc", "contributor", "theta_exact", "theta_decimal", "status"])
    for r in RECORDS:
        w.writerow([r[0], r[1], str(r[2]), f"{float(r[2]):.12f}", "Lean-verified record"])
    for r in CONDITIONAL:
        w.writerow([r[0], r[1], str(r[2]), f"{float(r[2]):.12f}", "conditional (H1-H5), not Lean-verified"])
print("wrote graphs/timeline.png and graphs/timeline.csv")
