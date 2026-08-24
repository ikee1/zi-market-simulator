from agents import StandardAgent
from orders import Order
from engine import LimitOrderBook

import numpy as np
import random

class Simulator:
    """
    Where the market simulation itself runs, controls time steps and agent generation etc.
    """
    def __init__(self):
        self.NUM_AGENTS = 500
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
            

        