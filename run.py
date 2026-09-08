from simulator import Simulator
import plots

import numpy as np
import matplotlib.pyplot as plt


NUM_RUNS = 10000
NUM_AGENTS = 100
NUM_REPEATS = 100


all_corrs = {N: [] for N in range(1, 11)}

for repeat in range(NUM_REPEATS):

    sim = Simulator()

    trades, _, _, _, imbalance_results = sim.run(
        NUM_RUNS,
        N_level_max=10,
        horizon=10,
        sampling_interval=10
    )

    for N in range(1, 11):

        results = imbalance_results[N-1]

        imbalances = [x[0] for x in results]
        returns = [x[1] for x in results]

        if len(results) >= 3:
            corr = np.corrcoef(imbalances, returns)[0, 1]
            all_corrs[N].append(corr)

means = []
stds = []

for N in range(1, 11):
    means.append(np.mean(all_corrs[N]))
    stds.append(np.std(all_corrs[N]))

fig, ax = plt.subplots()

levels = np.arange(1, 11)

ax.errorbar(
    levels,
    means,
    yerr=stds,
    marker='o',
    capsize=4
)

ax.axhline(0, linestyle='--')

ax.set_xlabel("Number of LOB levels")
ax.set_ylabel("Correlation: imbalance vs future return")
ax.set_title("Predictive power of order book imbalance")

plt.show()
for i in range(len(levels)):
    print(f"level: {levels[i]} -> mean_corr: {means[i]}")

