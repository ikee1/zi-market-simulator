from simulator import Simulator
import plots

import numpy as np
import matplotlib.pyplot as plt


NUM_RUNS = 10000
NUM_AGENTS = 100
NUM_REPEATS = 100

levels = np.arange(1, 10)
horizon = 10
interval = 10

sim = Simulator()

trades,_,_,_,imbalance_returns = sim.run(NUM_RUNS, levels[0], horizon, interval)

plots.plot_time_series_event_driven(trades, NUM_AGENTS, NUM_RUNS)
plt.show()

print(imbalance_returns[40:50])
imbalances = [x[0] for x in imbalance_returns]
returns = [x[1] for x in imbalance_returns]
fig, ax = plt.subplots()
ax.scatter(imbalances, returns, s=5)
plt.show()