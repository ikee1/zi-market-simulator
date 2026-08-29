"""
Zero-Intelligence trader
"""
import random
import numpy as np
from orders import Order, Trade
from maths import box_muller
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
    def __init__(self, order_std=50, fp_std=10):
        # std dev in pence
        super().__init__()
        self.std_dev = order_std
        self.fp_std_dev = fp_std
        self.current_price = 0

    def get_trade_price(self, previous_price, perceived_fundamental_price):
        rand = box_muller()  # random normal variable
        deviation = self.std_dev * rand
        return perceived_fundamental_price + deviation
    
    def get_fp(self, fundamental_price):
        # we need to change our belief of the fundamental price based on the std 
        rand = box_muller()
        dev = self.fp_std_dev * rand
        fundamental_price_dev = fundamental_price + dev
        return fundamental_price_dev
    
    def get_quantity(self, min: int, max: int):
        # quantity 100 to 1000 at 100 intervals
        num = np.random.randint(min/100, max/100)
        quantity = int(num * 100)
        return quantity

    def get_bid(self, prev_price, fundamental_price_dev):
        # buy if previous price too low, sell if previous price too high
        # we need to change our belief of the fundamental price based on the std 
        if prev_price is None or prev_price == fundamental_price_dev:
            return random.choice([True, False])
        if prev_price < fundamental_price_dev:
            return True
        elif prev_price > fundamental_price_dev:
            return False 

    def create_order(self, timestamp, previous_price, fundamental_price):
        perceived_fp = self.get_fp(fundamental_price)
        price = self.get_trade_price(previous_price, perceived_fp)
        quantity = self.get_quantity(100, 1000)
        bid = self.get_bid(previous_price, perceived_fp)

        order = Order(price, quantity, bid, timestamp)
        return order


        
    

