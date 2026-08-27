"""
Zero-Intelligence trader
"""
import random
import numpy as np
from orders import Order, Trade
import maths
import analysis

current_id = 0
class AgentBase:
    """
    The base class, all different personalities of trader will derive from this.
    """
    def __init__(self):
        # each agent should have an id (later add cash and inventory) 
        global current_id
        self.id = current_id
        current_id += 1
    
    def __repr__(self):
        return f"agent{self.id}"
    
class StandardAgent(AgentBase):
    """
    Very default test agent to see how things work
    """
    def __init__(self, std_dev=5):
        # std dev in pence
        super().__init__()
        self.std_dev = std_dev
        self.current_price = 0
    
    def set_price(self, default_price=100, previous_trade=None):
        # the agent will generate a random price within a couple of deviations of the 
        # previous trade's price
        z0 = maths.box_muller()
        dev = z0 * self.std_dev
        if previous_trade != None:
            self.current_price = round(previous_trade + dev)
        else:
            self.current_price = round(default_price + dev)

    def create_order(self, timestamp: int, prev_trade: Trade = None, fair_price = None):
        # create order object
        # first consider a random multiple of 100 between say 100 and 1000 inclusive
        count = 100 * np.random.randint(1, 11)
        # whether it is a bid or ask must depend on whether the previous trade is more or less than the
        # current fair value
        if prev_trade is None:
            self.set_price(previous_trade=prev_trade)
            num = random.randint(0,1)
            bid = True if num < 0.5 else False
            order = Order(self.current_price, count, bid, timestamp)
            return order
        prev_price = prev_trade.get_price()
        if prev_price < fair_price:
            bid = True # current price is lower than "fundamental" price, the agent will buy
        elif prev_price == fair_price:
            return None # don't trade if price is equal to the fundamental
        else:
            bid = False
        self.set_price(previous_trade=prev_price)
        order = Order(self.current_price, count,  bid, timestamp)
        return order
    
        # THOROUGHLY READ OVER THIS, MIGHT BE V WRONG.

