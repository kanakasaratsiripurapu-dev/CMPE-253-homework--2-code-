# CQ4 - PGD on a fixed linear model, checked against NQ8
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def pgd_attack(w, b, x0, y, eps, alpha, steps):
    w = np.asarray(w, float)
    x0 = np.asarray(x0, float)
    x = x0.copy()
    rows = []
    for t in range(steps + 1):
        f = w @ x + b
        p = sigmoid(f)
        loss = -np.log(p) if y == 1 else -np.log(1 - p)
        rows.append((t, x.copy(), f, p, loss))
        grad = (p - y) * w
        x = np.clip(x + alpha * np.sign(grad), x0 - eps, x0 + eps)
    return rows


rows = pgd_attack(w=(1, 2), b=-0.1, x0=(0.30, 0.20), y=1,
                  eps=0.4, alpha=0.1, steps=4)

print(f"{'t':>2} {'x_t':>18} {'f(x_t)':>8} {'p_t':>8} {'loss':>8}")
for t, x, f, p, loss in rows:
    # rounding then adding 0.0 hides the -0.0000 from float error
    x = np.round(x, 10) + 0.0
    xs = f"({x[0]:+.2f}, {x[1]:+.2f})"
    print(f"{t:>2} {xs:>18} {round(f, 10) + 0.0:>8.4f} {p:>8.4f} {loss:>8.4f}")

print(f"\nraw f(x_2) before rounding = {rows[2][2]:.3e}")

# values from my hand work in NQ8
hand = [(0.6, 0.6457, 0.4375), (0.3, 0.5744, 0.5544), (0.0, 0.5, 0.6931),
        (-0.3, 0.4256, 0.8544), (-0.6, 0.3543, 1.0375)]
ok = all(np.allclose([r[2], r[3], r[4]], h, atol=1e-4) for r, h in zip(rows, hand))
print("\nMatches hand computation from NQ8:", ok)

ts = [r[0] for r in rows]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
a1.plot(ts, [r[2] for r in rows], "o-")
a1.axhline(0, color="crimson", ls="--", lw=1, label="decision boundary f = 0")
a1.set_xlabel("Iteration t")
a1.set_ylabel("f(x_t)")
a1.set_title("Model output vs t")
a1.legend(fontsize=8)
a2.plot(ts, [r[4] for r in rows], "s-", color="tab:red")
a2.set_xlabel("Iteration t")
a2.set_ylabel("Loss = -ln(p)")
a2.set_title("Loss vs t")
for a in (a1, a2):
    a.set_xticks(ts)
    a.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("plots/cq4_pgd.png", dpi=150)
