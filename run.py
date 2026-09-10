
import numpy as np
import matplotlib.pyplot as plt

from simulator import Simulator
import plots

NUM_RUNS = 100000
NUM_AGENTS = 100
NUM_REPEATS = 15

s = 2 # interval between imbalance calculations
h = 2 # horizon that the returns are calculated over/position is held for after the 
# imbalance is calculated and a position is taken
N = 3 # number of levels of depth considered in the order book to calculate the imbalance from

all_rand_returns = []
all_sharpe_returns = []
for i in range(NUM_REPEATS):
    sim = Simulator()
    trades, _, _, imbalances, sharpe_returns, rand_returns = sim.run(NUM_RUNS, horizon=h, N_depth=N, sampling_interval=s)

    all_sharpe_returns.extend(sharpe_returns)
    all_rand_returns.extend(rand_returns)

mean_returns = np.mean(all_sharpe_returns)
std_returns = np.std(all_sharpe_returns)

mean_rand = np.mean(all_rand_returns)
std_rand = np.std(all_rand_returns)

print(f"Sharpe for the strategy is {mean_returns / std_returns}")
print(f"Sharpe for random control strategy is {mean_rand / std_rand}")
print(f"Mean returns is {mean_returns}")
print(f"Standard deviation of returns is {std_returns}")
print(f"Total observations is {len(all_sharpe_returns)}")  