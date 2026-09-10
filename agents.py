import random

import numpy as np

from orders import Order
from maths import box_muller

current_id = 0


class AgentBase:
    """
    Base class for all trader types in the simulation.
    """
    def __init__(self): 
        global current_id
        self.id = current_id
        current_id += 1
    
    def __repr__(self):
        return f"agent{self.id}"
    
class StandardAgent(AgentBase):
    """
    Trader that generates stochastic orders around a perceived
    fundamental price.

    Parameters
    ----------
    order_std : float
        Standard deviation in pence assigned to the normal distribution from which the agent's trade
        price is sampled, with a mean of the perceived fundamental price
    fp_std : float
        Standard deviation in pence assigned to the normal distribution from which the agent's perception of 
        the fundamental price is sampled, with a mean of the true fundamental price
    """
    def __init__(self, order_std=50, fp_std=10):
        super().__init__()
        self._order_std = order_std
        self._fp_std = fp_std

    def get_trade_price(self, perceived_fundamental_price):
        """Generate an order price around a perceived fundamental price"""
        rand = box_muller() 
        deviation = self._order_std * rand
        return perceived_fundamental_price + deviation
    
    def get_fp(self, fundamental_price):
        """Generate the agent's perceived fundamental price""" 
        rand = box_muller()
        deviation = self._fp_std * rand
        perceived_fundamental_price = fundamental_price + deviation
        return perceived_fundamental_price
    
    def get_quantity(self, min_quantity: int, max_quantity: int):
        """Generate a random order quantity in intervals of 100"""
        num = np.random.randint(min_quantity/100, max_quantity/100 + 100)
        quantity = int(num * 100)
        return quantity

    def get_bid(self, prev_price, perceived_fundamental_price):
        """
        Determine whether the agent submits a bid or ask based on its
        own perceived fundamental price
        """
        if prev_price is None or prev_price == perceived_fundamental_price:
            return random.choice([True, False])
        
        return prev_price < perceived_fundamental_price

    def create_order(self, timestamp, previous_price, fundamental_price):
        """
        Generate an order using the agent's perceived fundamental price

        Parameters
        ----------
        timestamp : int
            Current simulation time
        previous_price : int
            Most recent traded price
        fundamental_price : float
            Current true fundamental price
        
        Returns
        -------
        order : Order
            The generated order
        """
        perceived_fp = self.get_fp(fundamental_price)
        price = self.get_trade_price(perceived_fp)
        quantity = self.get_quantity(1000, 10000)
        bid = self.get_bid(previous_price, perceived_fp)

        order = Order(price, quantity, bid, timestamp)
        return order


        
    

