from agents import StandardAgent
from orders import Order, Trade
from engine import LimitOrderBook
from collections import deque

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

    def run(self, NUM_RUNS, horizon=2, N_depth=3, sampling_interval=2):
        fp = 10000  # initial fair price in pence
        fps = []
        diffs = []
        # implementation of horizon tests
        returns_sharpe = [] # for Sharpe ratio
        random_returns = []
        pending = deque()
        times = deque()
        imbalance_results = []
        trades_per_regime = np.zeros(int(np.ceil(NUM_RUNS/90)))
        for i in range(NUM_RUNS):
            if i > 0 and i % 90 == 0:
                fp += np.random.normal(0, 50)
            # sample
            if i > 50 and i % sampling_interval == 0:   
                if self.lob._asks_list and self.lob._bids_list:
                    midprice = self.lob.get_midprice()
                    # imbalance
                    bid_vol = self.lob.get_bid_volume(N_depth)
                    ask_vol = self.lob.get_ask_volume(N_depth)
                    imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol)
                    # position is:
                    # +ve if imbalance > threshold, indicating a long position
                    # negative if imbalance < -threshold, short position
                    # 0 if -threshold < imbalance < threshold, indicating no position taken
                    if imbalance == 0:
                        position = 0
                    else:
                        position = np.sign(imbalance)
                    rand_position = random.choice([-1, 0, 1])
                    pending.append((rand_position, position, imbalance, midprice))
                    times.append(i + horizon)
            # observation
            if times and i == times[0]: # check times[N] has anything in (since i = 0 is skipped for imbalance, so no times appended)
                if not self.lob._asks_list or not self.lob._bids_list:
                    times.popleft()
                    pending.popleft()
                    continue
                rand_position, position, imbalance, midprice = pending[0]

                midprice_t = self.lob.get_midprice() 
                log_return_t = np.log(midprice_t / midprice)

                imbalance_results.append((imbalance, log_return_t))
                returns_sharpe.append(position * log_return_t)
                random_returns.append(rand_position * log_return_t)
                times.popleft()
                pending.popleft()
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
        """for trade in trades:
            regime = trade.get_timestamp() // 90
            trades_per_regime[regime] += 1"""

        return trades, fps, mad, trades_per_regime, imbalance_results, returns_sharpe, random_returns
        

        

