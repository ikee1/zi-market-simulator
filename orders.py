import numpy as np # type: ignore
class Order: 
    """
    Holds the information on the orders placed to the book        
    """
    def __init__(self, price: int, count: int, bid: bool, time_submitted: int, tif = "gtd", expiry_time: int=None):
        self._price = price 
        self._count = count
        self._id = None
        self._bid = bid 
        self._timestamp = time_submitted
        self._tif = tif #expected: "ioc", "fok", "gtd", "gtc", maybe later try passing (tif, expiry_time as tuple)
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
        return self._price 

    def get_count(self):
        return self._count

    def get_type(self): #returns True for bids, False for asks
        return self._bid
    
    def get_timestamp(self):
        return self._timestamp
    
    def set_id(self, id):
        self._id = id

    def get_id(self):
        return self._id

    def add_count(self, count):
        self._count += count