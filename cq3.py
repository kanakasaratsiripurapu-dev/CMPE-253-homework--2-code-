# CQ3 - matching group G's TPR to group H by bisection
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def make_scores(n, base_rate, seed):
    rng = np.random.default_rng(seed)
    y = (rng.random(n) < base_rate).astype(int)
    s = np.clip(rng.normal(0.35 + 0.35 * y, 0.20), 0, 1)
    return y, s


y_G, s_G = make_scores(15000, 0.40, seed=11)  # Group G
y_H, s_H = make_scores(15000, 0.55, seed=12)  # Group H


def at_t(y, s, t):
    pred = s >= t
    tpr = (pred & (y == 1)).sum() / (y == 1).sum()
    fpr = (pred & (y == 0)).sum() / (y == 0).sum()
    return {"tpr": tpr, "fpr": fpr}


H_op = at_t(y_H, s_H, 0.5)
target = H_op["tpr"]
print(f"Group H at t = 0.5: TPR = {H_op['tpr']:.4f}, FPR = {H_op['fpr']:.4f}")
print(f"Target TPR for group G = {target:.4f}\n")

# TPR goes down as t goes up, so a TPR above target means t is too low
lo, hi = 0.01, 0.99
print(f"{'iter':>4} {'lo':>8} {'hi':>8} {'mid':>8} {'TPR(mid)':>10}")
for i in range(1, 11):
    mid = (lo + hi) / 2
    tpr_mid = at_t(y_G, s_G, mid)["tpr"]
    print(f"{i:>4} {lo:>8.4f} {hi:>8.4f} {mid:>8.4f} {tpr_mid:>10.4f}")
    if tpr_mid > target:
        lo = mid
    else:
        hi = mid

t_G = (lo + hi) / 2
G_op = at_t(y_G, s_G, t_G)
print(f"\nGroup G matched threshold t* = {t_G:.4f}")
print(f"Group G at t*: TPR = {G_op['tpr']:.4f}, FPR = {G_op['fpr']:.4f}")
print(f"TPR difference vs target = {G_op['tpr'] - target:+.4f}")


def roc(y, s):
    ts = np.linspace(0, 1, 201)
    pts = [at_t(y, s, t) for t in ts]
    return [p["fpr"] for p in pts], [p["tpr"] for p in pts]


fig, ax = plt.subplots(figsize=(5.5, 5))
fG, tG = roc(y_G, s_G)
fH, tH = roc(y_H, s_H)
ax.plot(fG, tG, label="Group G")
ax.plot(fH, tH, label="Group H")
ax.plot([0, 1], [0, 1], "k:", lw=1)
ax.scatter(H_op["fpr"], H_op["tpr"], s=70, marker="o", color="tab:orange",
           edgecolor="k", zorder=5, label=f"H at t = 0.50")
ax.scatter(G_op["fpr"], G_op["tpr"], s=90, marker="*", color="tab:blue",
           edgecolor="k", zorder=5, label=f"G at t* = {t_G:.3f}")
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.set_title("CQ3: ROC curves with matched TPR points")
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig("plots/cq3_roc.png", dpi=150)
