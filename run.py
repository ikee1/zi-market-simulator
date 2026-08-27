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

sim = Simulator(NUM_AGENTS)

trades = sim.run(NUM_RUNS)

plots.plot_time_series_event_driven(trades, NUM_AGENTS, NUM_RUNS)
plt.show()