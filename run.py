from simulator import Simulator
from orders import Order
from agents import StandardAgent
from engine import LimitOrderBook
import analysis
import plots
import time

import numpy as np
import matplotlib.pyplot as plt

NUM_RUNS = 10000
NUM_AGENTS = 100

order_price_deviation = 50
fp_deviations = np.arange(5, 105, 5)

avg_mads = []
for deviation in fp_deviations:
    mads = []
    for i in range(100):
        print(f"run {i} for {deviation}")
        sim = Simulator(NUM_AGENTS, std_deviation_agents=order_price_deviation, fp_std_deviation_agents=deviation)

        trades, fp, mad = sim.run(NUM_RUNS)
        mads.append(mad)
    avg_mad = np.mean(mads)
    avg_mads.append(avg_mad)

plots.plot_mad(fp_deviations, avg_mads)
plt.show()