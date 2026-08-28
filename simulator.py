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
    def __init__(self, num_agents=500, std_deviation_agents = 5):
        self.NUM_AGENTS = num_agents
        self.time = 0
        self.agents = []
        self.lob = LimitOrderBook()
        for i in range(self.NUM_AGENTS):
            agent = StandardAgent(std_dev=std_deviation_agents)
            self.agents.append(agent)

    def run(self, NUM_RUNS):
        fp = 100 #initial fair price
        fps = []
        for i in range(NUM_RUNS):
            if i % 90 == 0:
                fp += 2
            fps.append(fp)
            # select a random agent
            agent = random.choice(self.agents) # type: StandardAgent
            trades = self.lob.get_trades()
            if len(trades) == 0:
                prev_price = None
            else:
                prev_price = trades[-1].get_price()
            order = agent.create_order(self.time, prev_price, fp)
            if order is not None:
                self.lob.process_order(order)
            self.time += 1
        # self.lob.get_simple_bid_table()
        # self.lob.get_simple_ask_table()
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
        return trades, fps
        

        

