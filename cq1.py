# CQ1 - fairness metrics for three groups
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def fairness_metrics(tp, fp, tn, fn):
    n = tp + fp + tn + fn
    return {
        "selection_rate": (tp + fp) / n,
        "tpr": tp / (tp + fn),
        "fpr": fp / (fp + tn),
        "precision": tp / (tp + fp),
    }


groups = {
    "P": (80, 15, 160, 25),
    "Q": (55, 35, 95, 35),
    "R": (40, 20, 110, 30),
}
keys = ["selection_rate", "tpr", "fpr", "precision"]

results = {g: fairness_metrics(*c) for g, c in groups.items()}

print(f"{'Group':<6}" + "".join(f"{k:>16}" for k in keys))
for g, m in results.items():
    print(f"{g:<6}" + "".join(f"{m[k]:>16.4f}" for k in keys))

# pick the group whose selection rate sits in the middle
names = list(results)
sel = np.array([results[g]["selection_rate"] for g in names])
med_group = names[np.argsort(sel)[len(sel) // 2]]
print(f"\nMedian selection-rate group: {med_group} "
      f"({results[med_group]['selection_rate']:.4f})")

print(f"\nGaps vs {med_group} (other group minus {med_group}):")
print(f"{'Group':<6}" + "".join(f"{k:>16}" for k in keys))
for g in names:
    if g == med_group:
        continue
    gaps = [results[g][k] - results[med_group][k] for k in keys]
    print(f"{g:<6}" + "".join(f"{v:>+16.4f}" for v in gaps))

# grouped bar chart, TPR next to FPR for each group
x = np.arange(len(names))
wd = 0.35
tpr = [results[g]["tpr"] for g in names]
fpr = [results[g]["fpr"] for g in names]
fig, ax = plt.subplots(figsize=(6, 4))
b1 = ax.bar(x - wd / 2, tpr, wd, label="TPR")
b2 = ax.bar(x + wd / 2, fpr, wd, label="FPR")
ax.bar_label(b1, fmt="%.3f", fontsize=8)
ax.bar_label(b2, fmt="%.3f", fontsize=8)
ax.set_xticks(x, [f"Group {g}" for g in names])
ax.set_ylabel("Rate")
ax.set_xlabel("Group")
ax.set_ylim(0, 1)
ax.set_title("CQ1: TPR and FPR by group")
ax.legend()
fig.tight_layout()
fig.savefig("plots/cq1_bars.png", dpi=150)
