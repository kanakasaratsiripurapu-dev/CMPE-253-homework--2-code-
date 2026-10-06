import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# NQ2 gaps with 95% CI
names = ["Selection rate", "TPR", "FPR", "Precision"]
gap = np.array([0.1038, 0.0084, 0.1938, -0.2444])
se = np.array([0.0459, 0.0704, 0.0477, 0.0672])
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.errorbar(range(4), gap, yerr=1.96 * se, fmt="o", capsize=6, ms=7)
ax.axhline(0, color="k", ls="--", lw=1)
ax.set_xticks(range(4), names)
ax.set_ylabel("Gap (D - C)")
ax.set_xlabel("Metric")
ax.set_title("NQ2: metric gaps with 95% confidence intervals")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("plots/nq2_ci.png", dpi=150)

# NQ5 bisection
t = np.linspace(0, 1, 300)
mids = [0.5, 0.25, 0.375, 0.3125, 0.34375]
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(t, 1 - t ** 1.5, label="TPR_G(t) = 1 - t^1.5")
ax.axhline(0.8, color="gray", ls="--", lw=1, label="target TPR = 0.80")
for i, m in enumerate(mids, 1):
    ax.scatter(m, 1 - m ** 1.5, zorder=5, color="crimson")
    ax.annotate(str(i), (m, 1 - m ** 1.5), xytext=(5, 5), textcoords="offset points")
ax.axvline(0.2 ** (2 / 3), color="green", ls=":", label="exact t* = 0.342")
ax.set_xlabel("Threshold t"); ax.set_ylabel("TPR of group G")
ax.set_title("NQ5: bisection midpoints (numbered by iteration)")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("plots/nq5_bisect.png", dpi=150)

# NQ6 expected vs actual, plus cumulative with KS gap
e = np.array([.15, .25, .30, .20, .10]); a = np.array([.10, .20, .28, .24, .18])
bins = np.arange(1, 6)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
a1.bar(bins - 0.2, e, 0.4, label="Expected"); a1.bar(bins + 0.2, a, 0.4, label="Actual")
a1.set_xlabel("Bin"); a1.set_ylabel("Proportion"); a1.set_title("Bin proportions"); a1.legend()
ce, ca = np.cumsum(e), np.cumsum(a)
a2.step(bins, ce, where="mid", marker="o", label="Cumulative expected")
a2.step(bins, ca, where="mid", marker="s", label="Cumulative actual")
a2.vlines(3, ca[2], ce[2], color="crimson", lw=3, label="KS = 0.12 (bin 3)")
a2.set_xlabel("Bin"); a2.set_ylabel("Cumulative proportion"); a2.set_title("Cumulative distributions")
a2.legend(fontsize=8)
fig.tight_layout(); fig.savefig("plots/nq6_drift.png", dpi=150)

# NQ7 loss curve
J = [0.6931, 0.4741, 0.3477, 0.2700]
fig, ax = plt.subplots(figsize=(5.5, 3.6))
ax.plot(range(4), J, "o-")
for i, v in enumerate(J): ax.annotate(f"{v:.4f}", (i, v), xytext=(5, 5), textcoords="offset points")
ax.set_xticks(range(4)); ax.set_xlabel("Iteration t"); ax.set_ylabel("Loss J")
ax.set_title("NQ7: training loss vs iteration"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("plots/nq7_loss.png", dpi=150)

# NQ8 f and loss
f = [0.6, 0.3, 0.0, -0.3, -0.6]; L = [0.4375, 0.5544, 0.6931, 0.8544, 1.0375]
fig, ax = plt.subplots(figsize=(6, 3.8))
ax.plot(range(5), f, "o-", label="f(x_t)")
ax.plot(range(5), L, "s-", color="tab:red", label="loss -ln(p_t)")
ax.axhline(0, color="k", ls="--", lw=1)
ax.set_xticks(range(5)); ax.set_xlabel("PGD iteration t"); ax.set_ylabel("Value")
ax.set_title("NQ8: model output and loss during the attack"); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig("plots/nq8_pgd.png", dpi=150)

# NQ9 log-log
T = np.array([100, 200, 300, 400, 500])
fig, ax = plt.subplots(figsize=(6, 4))
ax.loglog(T, 0.03 * T, "o-", label="basic: 0.03 T")
ax.loglog(T, 0.15 * np.sqrt(T), "s-", label="tight: 0.15 sqrt(T)")
ax.set_xlabel("Training steps T (log scale)"); ax.set_ylabel("epsilon (log scale)")
ax.set_title("NQ9: privacy loss under two accounting methods")
ax.legend(); ax.grid(which="both", alpha=0.3)
fig.tight_layout(); fig.savefig("plots/nq9_loglog.png", dpi=150)

# NQ10 PPV vs FPR and recall bars
fprs = np.array([0.05, 0.01, 0.005, 0.001]); pi = 2e-4
ppv = pi * 0.9 / (pi * 0.9 + (1 - pi) * fprs)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
a1.semilogx(fprs, ppv, "o-")
for x_, y_ in zip(fprs, ppv): a1.annotate(f"{y_:.4f}", (x_, y_), xytext=(4, 4), textcoords="offset points", fontsize=8)
a1.set_xlabel("False positive rate (log scale)"); a1.set_ylabel("PPV"); a1.set_title("PPV vs FPR (TPR = 0.90)")
a1.grid(which="both", alpha=0.3)
bars = a2.bar(["Single detector", "Two-stage cascade"], [0.90, 0.931], color=["tab:gray", "tab:green"])
a2.bar_label(bars, fmt="%.3f"); a2.set_ylim(0.8, 1.0); a2.set_ylabel("Recall"); a2.set_title("Recall at overall FPR = 0.1%")
fig.tight_layout(); fig.savefig("plots/nq10_ppv.png", dpi=150)
