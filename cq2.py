# CQ2 - bootstrap test for a metric gap between groups C and D
import numpy as np
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(253)


def metric_from_counts(c, metric):
    # c has columns tp, fp, tn, fn (works on one row or many rows)
    tp, fp, tn, fn = c[..., 0], c[..., 1], c[..., 2], c[..., 3]
    with np.errstate(divide="ignore", invalid="ignore"):
        if metric == "selection_rate":
            return (tp + fp) / (tp + fp + tn + fn)
        if metric == "tpr":
            return tp / (tp + fn)
        if metric == "fpr":
            return fp / (fp + tn)
        if metric == "precision":
            return tp / (tp + fp)
    raise ValueError(metric)


def bootstrap_gap(counts_a, counts_b, metric, B=20000):
    a = np.asarray(counts_a)
    b = np.asarray(counts_b)
    # resample each group's four cells, keeping that group's N fixed
    ra = rng.multinomial(a.sum(), a / a.sum(), size=B)
    rb = rng.multinomial(b.sum(), b / b.sum(), size=B)
    diffs = metric_from_counts(rb, metric) - metric_from_counts(ra, metric)
    return diffs[np.isfinite(diffs)]


C = (72, 18, 140, 30)
D = (50, 40, 90, 20)

summary = {}
for metric in ["fpr", "selection_rate"]:
    obs = metric_from_counts(np.array(D), metric) - metric_from_counts(np.array(C), metric)
    d = bootstrap_gap(C, D, metric)
    sd = d.std(ddof=1)
    lo, hi = np.percentile(d, [2.5, 97.5])
    z = obs / sd
    p = 2 * norm.sf(abs(z))
    summary[metric] = (obs, sd, lo, hi, z, p, d)
    print(f"--- {metric} gap (D - C) ---")
    print(f"observed gap      : {obs:.4f}")
    print(f"bootstrap SD      : {sd:.4f}")
    print(f"95% percentile CI : [{lo:.4f}, {hi:.4f}]")
    print(f"z = gap / SD      : {z:.3f}")
    print(f"approx. p-value   : {p:.2e}\n")

for m in summary:
    print(f"{m:<15} z = {summary[m][4]:.2f}")

obs, sd, lo, hi, z, p, d = summary["fpr"]
fig, ax = plt.subplots(figsize=(6.5, 4))
ax.hist(d, bins=60, color="#8fb3d9", edgecolor="white")
ax.axvline(obs, color="crimson", lw=2, label=f"observed gap = {obs:.3f}")
ax.axvline(0, color="black", ls="--", lw=1.5, label="zero (no gap)")
ax.axvspan(lo, hi, color="orange", alpha=0.15, label="95% percentile CI")
ax.set_xlabel("Bootstrapped FPR gap (D - C)")
ax.set_ylabel("Count of resamples")
ax.set_title("CQ2: bootstrap distribution of the FPR gap (B = 20,000)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig("plots/cq2_hist.png", dpi=150)
