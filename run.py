from simulator import Simulator
from orders import Order
from agents import StandardAgent
from engine import LimitOrderBook

import numpy as np
import matplotlib.pyplot as plt

simulation = Simulator(num_agents = 100)


averages = []
for i in range(10):
    trades = simulation.run(10000)
    prices = [trade.get_price() for trade in trades]
    averages.append(np.sum(prices[-20:]) / 20) # average of the last 20 trade prices, to see where it converges
indices = np.arange(len(averages))

fig, ax1 = plt.subplots()

ax1.set_xlabel("run")
ax1.set_ylabel("final price") # could alter this to test for convergence by having price last ten trades/price last 100 trades sort of thing and if it's 1 it is convergent
ax1.scatter(indices, averages, color="blue")
plt.show()

