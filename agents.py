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
    def __init__(self, std_dev=5):
        # std dev in pence
        super().__init__()
        self.std_dev = std_dev
        self.current_price = 0

    def get_trade_price(self, previous_price, fundamental_price):
        rand = box_muller()  # random normal variable
        deviation = self.std_dev * rand
        if previous_price is None:
            return np.round(fundamental_price + deviation)
        return np.round(previous_price + deviation)
    
    def get_quantity(self, min: int, max: int):
        # quantity 100 to 1000 at 100 intervals
        num = np.random.randint(min/100, max/100)
        quantity = int(num * 100)
        return quantity

    def get_bid(self, prev_price, fundamental_price):
        if prev_price is None or prev_price == fundamental_price:
            return random.choice([True, False])
        # buy if previous price too low, sell if previous price too high
        if prev_price < fundamental_price:
            return True
        elif prev_price > fundamental_price:
            return False 

    def create_order(self, timestamp, previous_price, fundamental_price):
        price = self.get_trade_price(previous_price, fundamental_price)
        quantity = self.get_quantity(100, 1000)
        bid = self.get_bid(previous_price, fundamental_price)

        order = Order(price, quantity, bid, timestamp)
        return order


        
    

