import random
from collections import deque

import numpy as np

from agents import StandardAgent
from orders import Order, Trade
from engine import LimitOrderBook

class Simulator:
    """
    Controls the progression of the market simulation and initialisation of trading agents.

    Parameters
    ----------
    num_agents : int
        The number of agents to initialise in the simulation.
    std_agents : float
        Standard deviation assigned to the normal distribution which the agent's order price
        is sampled from, with the mean being the agent's interpretation of the fundamental price.
    fp_std_agents : float
        Standard deviation assigned to the normal distribution which the agent's interpretation of the
        fundamental price is sampled from, with the mean being the current fundamental price.
    """
    def __init__(self, num_agents=500, std_agents=50, fp_std_agents=10):
        self._NUM_AGENTS = num_agents
        self._time = 0
        self._agents = []
        self._lob = LimitOrderBook()
        for i in range(self._NUM_AGENTS):
            agent = StandardAgent(order_std=std_agents, fp_std=fp_std_agents)
            self._agents.append(agent)

    def run(self, num_runs, horizon=2, N_depth=3, sampling_interval=2):
        """
        Run the market simulation and evaluate the order book imbalance

        Parameters
        ----------
        num_runs : int
            Number of timesteps to run the simulation for.
        horizon : int
            Number of steps ahead over which future returns are measured.
        N_depth : int
            Number of order book levels used to calculate imbalance.
        sampling_interval : int
            Number of steps between imbalance calculations.
        """
        fp = 10000  # initial fair price in pence
        fps = []
        diffs = []
        
        returns_sharpe = [] # for Sharpe ratio
        random_returns = [] # control for random positions
        pending = deque()
        times = deque()
        imbalance_results = []

        for i in range(num_runs):
            if i > 0 and i % 90 == 0:
                fp += np.random.normal(0, 50)
            # sample
            if i > 50 and i % sampling_interval == 0:   
                if self._lob._asks_list and self._lob._bids_list:
                    midprice = self._lob.get_midprice()
                    # imbalance
                    bid_vol = self._lob.get_bid_volume(N_depth)
                    ask_vol = self._lob.get_ask_volume(N_depth)
                    imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol)

                    # position +1 if imbalance +ve, indicating a long position,
                    # -1 if imbalance is -ve, indicating a short position
                    position = np.sign(imbalance)
                    rand_position = random.choice([-1, 0, 1])

                    pending.append((rand_position, position, imbalance, midprice))
                    times.append(i + horizon)
            
            # observation
            if times and i == times[0]:  # confirm times is not empty, since first sample is after i = 50
                if not self._lob._asks_list or not self._lob._bids_list:
                    times.popleft()
                    pending.popleft()
                    continue

                rand_position, position, imbalance, midprice = pending[0]

                midprice_t = self._lob.get_midprice() 
                log_return_t = np.log(midprice_t / midprice)

                imbalance_results.append((imbalance, log_return_t))
                returns_sharpe.append(position * log_return_t)
                random_returns.append(rand_position * log_return_t)

                times.popleft()
                pending.popleft()

            fps.append(fp)

            # select a random agent
            agent = random.choice(self._agents)

            trades = self._lob.get_trades()
            if len(trades) == 0:
                prev_price = None
            else:
                prev_price = trades[-1].get_price()
            order = agent.create_order(self._time, prev_price, fp)
            if order is not None:
                new_trades = self._lob.process_order(order) 
            self._time += 1
            for trade in new_trades:
                diff = np.abs(trade.get_price() - fp)   
                diffs.append(diff)
            
        trades = self._lob.get_trades()
        mad = np.mean(diffs)

        return trades, fps, mad, imbalance_results, returns_sharpe, random_returns
        

        

