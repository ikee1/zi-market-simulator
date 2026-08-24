"""
Zero-Intelligence trader
"""
import random
import numpy as np
from orders import Order
import maths

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
    
    def set_fair_price(self, previous_trade):
        # current fair price will be previous trade's price
        # plus some deviation defined by internal standard deviation
        # setup a normal distribution use box-muller
        z0 = maths.box_muller()
        dev = z0 * self.std_dev
        self.current_price = previous_trade + dev

    def create_order(self):
        # create order object
        # first consider a random multiple of 100 between say 100 and 1000 inclusive
        count = 100 * np.random.randint(1, 11)
        # for creation of random boolean for bid or ask
        rand_num = np.random.randint(0, 2)
        bid = True if rand_num < 0.5 else False
        order = Order(self.current_price, count,  bid)
        return order
    
        # THOROUGHLY READ OVER THIS, MIGHT BE V WRONG.

