import numpy as np 
class Order: 
    """
    Represents an order submitted to the limit order book
    
    Parameters
    ----------
    price : int
        Order price in pence
    count : int
        Number of units in the order
    bid : bool
        True for a bid (buy order) and False for an ask (sell order)
    time_submitted : int
        Simulation time at which the order was submitted
    tif : str, optional
        Time-in-force parameter. Expected values are "ioc", "fok", 
        "gtd", or "gtc". Default is "gtd"
    expiry_time : int, optional
        Simulation time at which a GTD order expires
    """
    def __init__(self, price: int, count: int, bid: bool, time_submitted: int, tif="gtd", expiry_time: int=None):
        self._price = price  # in pence
        self._count = count
        self._id = None
        self._bid = bid 
        self._timestamp = time_submitted
        self._tif = tif 
        if self._tif == "gtd":
            self._expiry_time = expiry_time
        elif self._tif == "gtc":
            self._expiry_time = np.inf
        elif self._tif == "ioc" or self._tif == "fok":
            self._expiry_time = 0

    def __repr__(self): 
        if self._id is None:
            return "order pending"
        return f"order{self._id}"
    
    def get_price(self):
        """Return the price of the order in pence"""
        return self._price 

    def get_count(self):
        """Return the quantity of the order"""
        return self._count

    def get_type(self):
        """Return True for bids, False for asks"""
        return self._bid
    
    def get_timestamp(self):
        """Return simulation time at which order was submitted"""
        return self._timestamp
    
    def set_id(self, id):
        """Assign the ID to the order"""
        self._id = id

    def get_id(self):
        """Return the ID of the order"""
        return self._id

    def add_count(self, count):
        """Increase the order quantity by a specified amount (works with negative input for subtractions)"""
        self._count += count

class Trade:
    """
    Represents a completed trade

    Parameters
    ----------
    price : int
        The price in pence the trade was carried out at
    count : int
        The number of units traded
    timestamp : int
        Simulation time at which the trade occurred
    """
    def __init__(self, price: int, count: int, timestamp: int):
        self._price = price 
        self._count = count
        self._timestamp = timestamp

    def get_price(self):
        """Return the price of the trade"""
        return self._price
    
    def get_count(self):
        """Return the quantity of units in the trade"""
        return self._count
    
    def get_timestamp(self):
        """Return the simulation time at which the trade was completed"""
        return self._timestamp
