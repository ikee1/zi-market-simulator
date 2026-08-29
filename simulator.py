from agents import StandardAgent
from orders import Order, Trade
from engine import LimitOrderBook

import numpy as np
import random
import matplotlib.pyplot as plt

class Simulator:
    """
    Where the market simulation itself sits, controls time steps and agent generation etc.
    """
    def __init__(self, num_agents=500, std_deviation_agents=50, fp_std_deviation_agents=10):
        self.NUM_AGENTS = num_agents
        self.time = 0
        self.agents = []
        self.lob = LimitOrderBook()
        for i in range(self.NUM_AGENTS):
            agent = StandardAgent(order_std=std_deviation_agents, fp_std=fp_std_deviation_agents)
            self.agents.append(agent)

    def run(self, NUM_RUNS):
        fp = 10000  # initial fair price in pence
        fps = []
        diffs = []
        for i in range(NUM_RUNS):
            """if i > 0 and i % 90 == 0:
                fp += 200"""
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
                new_trades = self.lob.process_order(order) #type: Trade
            self.time += 1
            for trade in new_trades:
                diff = np.abs(trade.get_price() - fp)
                diffs.append(diff)
        trades = self.lob.get_trades()
        mad = np.mean(diffs)
        return trades, fps, mad
        

        

