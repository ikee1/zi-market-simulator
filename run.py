from simulator import Simulator
from orders import Order
from agents import StandardAgent
from engine import LimitOrderBook
import analysis
import plots

import numpy as np
import matplotlib.pyplot as plt

NUM_RUNS = 1000
NUM_AGENTS = 100

"""deviations = np.arange(0.5, 10.5, 0.5)

avg_volatilities = []
std_devs = []
for deviation in deviations:
    volatilities = []
    for i in range(100):
        sim = Simulator(NUM_AGENTS, std_deviation_agents=deviation)
        print(f"{i}th run of {deviation}")
        trades = sim.run(NUM_RUNS)
        volatilities.append(analysis.calculate_volatility(trades))
    avg = sum(volatilities) / len(volatilities)
    std_dev = np.std(volatilities)
    avg_volatilities.append(avg)
    std_devs.append(std_dev)

fig, ax = plt.subplots()

ax.set_xlabel("Standard deviation of agents")
ax.set_ylabel("Volatility")
ax.errorbar(deviations, avg_volatilities, yerr=std_devs, color="blue")
ax.set_title("Volatility against agent standard deviation")
plt.show()"""

deviations = np.linspace(0.5, 10, 20)
avg_nums = []
avg_diffs = []
avg_within = []
for deviation in deviations:
    nums_of_trades = []
    final_diffs = []
    first_close_timesteps = []
    for i in range(10):
        sim = Simulator(NUM_AGENTS, std_deviation_agents=deviation)
        trades, fps = sim.run(NUM_RUNS)
        num_trades = len(trades)
        final_diff = trades[-1].get_price() - fps[-1]
        diffs = []
        for trade in trades:
            for j in range(len(fps)):
                if trade.get_timestamp() == j:
                    diff = trade.get_price() - fps[j]
                    if np.abs(diff) <= 2:
                        diffs.append(j)
        if len(diffs) != 0:
            first_diff = np.min(diffs)
            first_close_timesteps.append(first_diff)
        nums_of_trades.append(num_trades)
        final_diffs.append(final_diff)
    avg_nums.append(np.average(nums_of_trades))
    avg_diffs.append(np.average(final_diffs))
    avg_within.append(np.average(first_close_timesteps))

print(len(avg_nums))
fig, ax = plt.subplots()
ax.plot(deviations, avg_nums, "blue")
ax.set_title("avg number of trades")
ax.set_ylabel("num trades")
ax.set_xlabel("std deviation")
fig, ax2 = plt.subplots()
ax2.plot(deviations, avg_diffs)
ax2.set_title("average difference between final trade and final fundamental value")
ax2.set_xlabel("std deviation")
ax2.set_ylabel("final difference")
fig, ax3 = plt.subplots()
ax3.plot(deviations, avg_within)
ax3.set_title("number of runs to get within 2")
ax3.set_xlabel("std deviation")
ax3.set_ylabel("avg number of trades to first get within £2 of the fundamental value")
plt.show()

