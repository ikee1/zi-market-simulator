"""from engine import LimitOrderBook
from models import Order

book = LimitOrderBook()
bid1 = Order(105, 1000, True, "gtd", 3600)
bid2 = Order(106, 500, True, "gtd", 3600)
ask1 = Order(106, 2000, False, "gtd", 3600)
ask2 = Order(107, 2000, False, "gtd", 3600)
ask3 = Order(105, 1700, False, "gtd", 3600)

book.match_and_add_ask(ask1)
book.match_and_add_ask(ask2)
print("debug")
print(book._asks_list)
book.match_and_add_bid(bid1)
print(f"adding bid2")
book.match_and_add_bid(bid2)
book.match_and_add_ask(ask3)

print(f"asks: {book.get_asks()}")
print(f"bids: {book.get_bids()}")

print(f"ask prices: {book._asks_list}")
print(f"bid prices: {book._bids_list}")
print(f"count on ask at 106: {ask1.get_count()}") 
print(f"count on bid at 106: {bid2.get_count()}") 
print(f"count on ask at 105: {ask3.get_count()}")"""
"""from sortedcontainers import SortedList
from collections import deque, defaultdict
x = SortedList([1, 2, 4, 3, 5, 6])
dict = defaultdict(deque)
order1 = "order1"
order2 = "order2"
dict[104].append(order1)
dict[104].append(order2)
print(dict[104])

existing_key = dict[104]
print(existing_key[1])

existing_key.popleft()
print(dict[104])"""
from engine import LimitOrderBook
from orders import Order
from agents import StandardAgent

"""# 1. Initialize the book
book = LimitOrderBook()

# 2. Add two separate buyers (Bids) at different prices
# Buyer A wants 10 units at £100
bid_high = Order(price=100, count=10, bid=True)
# Buyer B wants 10 units at £90
bid_low = Order(price=90, count=10, bid=True)

book.process_order(bid_high)
book.process_order(bid_low)

print("--- BEFORE MATCHING ---")
print(f"Active bid price levels in book: {list(book._bids_list)}")
print(f"Bids dictionary state: {dict(book._bids)}")
print("-" * 25)

# 3. Send in an incoming Seller (Ask) that should eat the first buyer completely,
# but CANNOT match the second buyer because its selling price is too high.
# Seller wants to sell 15 units at £95.
incoming_ask = Order(price=95, count=15, bid=False)

print("\nProcessing incoming Ask (15 units @ £95)...")
book.process_order(incoming_ask)
print("-" * 25)

print("\n--- AFTER MATCHING ---")
print(f"Remaining ask price levels: {list(book._asks_list)}")
print(f"Remaining ask details: {dict(book._asks)}")
print(f"Remaining bid price levels: {list(book._bids_list)}")
print(f"Remaining bid details: {dict(book._bids)}")"""

NUM_AGENTS = 5
agents = []
for i in range(NUM_AGENTS):
    agent = StandardAgent()
    agents.append(agent)

print(agents)

agentA = agents[0]

order = agentA.create_order(1)
print(order.get_price(), order)
