from simulator import Simulator
import plots

import numpy as np
import matplotlib.pyplot as plt


NUM_RUNS = 100000
NUM_AGENTS = 100
NUM_REPEATS = 15

s = 2
h = 2
N = 3

all_rand_returns = []
all_sharpe_returns = []
for i in range(NUM_REPEATS):
    sim = Simulator()
    trades, _, _, _, imbalances, sharpe_returns, rand_returns = sim.run(NUM_RUNS, horizon=h, N_depth=N, sampling_interval=s)
    # we are calculating mean returns over a period
    # but since it is better to take all the returns and average them rather than averaging the Sharpes from each simulation,
    # I will extend them all into one long list
    all_sharpe_returns.extend(sharpe_returns)
    all_rand_returns.extend(rand_returns)

mean_returns = np.mean(all_sharpe_returns)
std_returns = np.std(all_sharpe_returns)

mean_rand = np.mean(all_rand_returns)
std_rand = np.std(all_rand_returns)

print(f"sharpe is {mean_returns / std_returns}")
print(f"for random strategy, Sharpe is {mean_rand / std_rand}")
print(mean_returns)
print(std_returns)
print(mean_returns / std_returns)
print(len(all_sharpe_returns))