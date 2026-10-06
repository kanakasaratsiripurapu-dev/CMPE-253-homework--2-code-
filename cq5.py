# CQ5 - sequential Bayesian update in log-odds form
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def bayes_update(prior, evidence):
    log_odds = np.log(prior / (1 - prior))
    out = [(0, "prior", None, np.exp(log_odds), prior)]
    for i, (name, lr) in enumerate(evidence, start=1):
        log_odds += np.log(lr)
        odds = np.exp(log_odds)
        out.append((i, name, lr, odds, odds / (1 + odds)))
    return out


evidence = [
    ("Burst of near-duplicate queries", 4.0),
    ("Off-hours access", 1.5),
    ("Known-good API key", 0.4),
    ("Grid-like systematic probing", 8.0),
]

rows = bayes_update(0.02, evidence)
print(f"{'step':>4}  {'evidence':<33}{'LR':>5}{'odds':>10}{'posterior':>11}")
for step, name, lr, odds, post in rows:
    lr_s = "-" if lr is None else f"{lr:.1f}"
    print(f"{step:>4}  {name:<33}{lr_s:>5}{odds:>10.4f}{post:>11.4f}")

first = next((r for r in rows if r[4] > 0.5), None)
if first:
    print(f"\nPosterior first passes 0.50 at step {first[0]} ({first[1]}), P = {first[4]:.4f}")
else:
    peak = max(rows, key=lambda r: r[4])
    print(f"\nPosterior never passes 0.50. Highest value is {peak[4]:.4f} "
          f"at step {peak[0]} ({peak[1]})")

for prev, cur in zip(rows, rows[1:]):
    if cur[4] < prev[4]:
        drop = (prev[4] - cur[4]) * 100
        print(f"'{cur[1]}' pulls the posterior down from {prev[4]:.4f} "
              f"to {cur[4]:.4f}, a drop of {drop:.2f} percentage points")

steps = [r[0] for r in rows]
post = [r[4] for r in rows]
fig, ax = plt.subplots(figsize=(7.5, 4.2))
ax.plot(steps, post, "o-", lw=2)
ax.axhline(0.5, color="crimson", ls="--", label="action threshold 0.50")
for s, p, name in zip(steps, post, [r[1] for r in rows]):
    ax.annotate(f"{name}\n{p:.3f}", (s, p), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=7.5)
ax.set_xlabel("Evidence step")
ax.set_ylabel("P(attack | evidence so far)")
ax.set_xticks(steps)
ax.set_ylim(0, 0.75)
ax.set_xlim(-0.6, 4.6)
ax.set_title("CQ5: posterior risk after each piece of evidence")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig("plots/cq5_posterior.png", dpi=150)
