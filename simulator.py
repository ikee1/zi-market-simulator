from agents import StandardAgent
from orders import Order
from engine import LimitOrderBook

import numpy as np
import random
import matplotlib.pyplot as plt

class Simulator:
    """
    Where the market simulation itself sits, controls time steps and agent generation etc.
    """
    def __init__(self, num_agents=500):
        self.NUM_AGENTS = num_agents
        self.time = 0
        self.agents = []
        self.lob = LimitOrderBook()
        for i in range(self.NUM_AGENTS):
            agent = StandardAgent()
            self.agents.append(agent)

    def run(self, NUM_RUNS):
        for i in range(NUM_RUNS):
            # select a random agent
            agent = random.choice(self.agents)
            trades = self.lob.get_trades()
            order = agent.create_order(self.time, prev_price=trades[-1].get_price()) if len(trades) != 0 else agent.create_order(self.time)
            self.lob.process_order(order)
            self.time += 1
        self.lob.get_simple_bid_table()
        self.lob.get_simple_ask_table()
        trades = self.lob.get_trades()

        # processing trades
        # prices = []
        # differences = []
        # for i in range(len(trades)):
            # prices.append(trades[i].get_price())
            # diff = trades[i].get_price() - trades[i-1].get_price() if i != 0 else 0
            # differences.append(diff)

        # indices = np.arange(len(prices))
        #fig, ax1 = plt.subplots()

        #ax1.set_ylabel("price/GBP")
        #ax1.set_xlabel("trade event")
        #ax1.plot(indices, prices, "blue")
        #ax1.set_title(f"no. of runs: {NUM_RUNS}\nno. agents: {self.NUM_AGENTS}\nfair price: £100")

        #fig, ax2 = plt.subplots()
        #ax2.plot(indices, differences, "red")

        # plt.show()
        return trades
        

        

