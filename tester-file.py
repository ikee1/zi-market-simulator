from maths import box_muller
import matplotlib.pyplot as plt
import numpy as np
from sortedcontainers import SortedList
from engine import LimitOrderBook
from orders import Order

import random

lob = LimitOrderBook()

ask1 = Order(100, 1080, False, 0)
ask2 = Order(101, 1000, False, 0)

bid1 = Order(99, 1000, True, 0)
bid2 = Order(98, 1000, True, 0)

lob.add_ask(ask1)
lob.add_ask(ask2)
lob.add_bid(bid1)
lob.add_bid(bid2)

lob.get_simple_ask_table()
lob.get_simple_bid_table()

mid = lob.get_midprice()
print(mid)

print(lob._asks[100])
print(lob.get_ask_volume(100))
print(lob.get_bid_volume(100))
list = [1,2,3,4,5,6] 
sum = np.sum(list) # should be 21
print(sum)
levels = np.arange(1, 11)

print(levels)

horizons = [5, 10, 20, 30, 50]
all_corrs = {horizon: [] for horizon in horizons}
print(all_corrs)
