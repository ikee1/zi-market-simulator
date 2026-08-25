from orders import Order, Trade
from collections import deque, defaultdict
from sortedcontainers import SortedList
class LimitOrderBook:
    """
    Limit Order Book object
    """
    def __init__(self):  # implement books for specific ticker later
        self._bids = defaultdict(deque)
        self._asks = defaultdict(deque)
        self._bids_list = SortedList([])
        self._asks_list = SortedList([])  # list all available keys for bids/asks
        self._completed_trades = []
        self._next_id = 1
        self._order_ids = []

    def process_order(self, order: Order):
        """
        Identifies an incoming order as a bid or an ask. Processes as required
        
        :param order: The incoming order to match against the book
        :type order: Order
        """
        if order.get_type() == True:
            self.match_and_add_bid(order)
        else:
            self.match_and_add_ask(order)
        return
    
    def match_and_add_bid(self, order: Order):
        # logic for matching incoming bids, then add to book whatever is left
        # bit uncertain about adding an order with less count, maybe juse use a reduce count/set count method or smth?
        while order.get_count() > 0 and order.get_id() not in self._order_ids:  # is this check even needed?? oh i spose so
            #print("check started")
            if len(self._asks_list) == 0:  # if no asks in book, simply add the bid directly
                # and exit while loop
                self.add_bid(order)
                break
            matching_key = self._asks[self._asks_list[0]]
            if order.get_price() >= self._asks_list[0] and len(self._asks_list) > 0: # cheapest ask is index 0
                existing_count = matching_key[0].get_count()
                diff = order.get_count() - existing_count  # difference between 
                # the oldest order on the key and the incoming order
                if diff > 0: # is incoming order bigger than biggest existing order
                    order.add_count(-existing_count) # take the counts from existing ask from the counts of the incoming bid
                    # remove order from dictionary
                    # and remove counts (will be zero)
                    trade = Trade(matching_key[0].get_price(), existing_count, order.get_timestamp())
                    self._completed_trades.append(trade)
                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()
                    # check dictionary, does it still have any elements left in that key?
                    # if so, remove that price from asks list
                    # this will NEVER be the case actually because since diff > 0, there 
                    # will always be an order left, the one we're adding
                    if len(matching_key) == 0:
                        del self._asks[self._asks_list[0]]
                        self._asks_list.pop(0)
                    #order must only enter the book if it has a matching count
                elif diff < 0:
                    # existing order is bigger than (or equal to) incoming order, 
                    # order will never enter the book, will be completely used up
                    # remove counts from existing order
                    matching_key[0].add_count(-order.get_count())
                    trade = Trade(matching_key[0].get_price(), order.get_count(), order.get_timestamp())
                    self._completed_trades.append(trade)
                    #still need to add order id to list (in case cancellation? although maybe not relevant here)
                    order.add_count(-order.get_count())
                    order.set_id(self._next_id)
                    self._order_ids.append(self._next_id)
                    self._next_id += 1
                else: # diff == 0 case
                    order.add_count(-existing_count)
                    trade = Trade(matching_key[0].get_price(), order.get_count(), order.get_timestamp())
                    self._completed_trades.append(trade)
                    #still need to add order id to list
                    order.set_id(self._next_id)
                    self._order_ids.append(self._next_id)
                    self._next_id += 1
                    # remove that order from dictionary
                    # and remove from asks list
                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()
                    if len(matching_key) == 0:
                        del self._asks[self._asks_list[0]]
                        self._asks_list.pop(0)
            else:
                # order must just be placed in book
                self.add_bid(order)
                break
    
    def match_and_add_ask(self, order: Order):
        # next job 
        while order.get_count() > 0 and order.get_id() not in self._order_ids:
            #logic, very similar, calculate difference etc etc.
            #print(f"check started")
            if len(self._bids_list) == 0:
                self.add_ask(order)
                break
            matching_key = self._bids[self._bids_list[-1]]  # best bid is last in list (lowest at 0, highest at -1)
            if order.get_price() <= self._bids_list[-1] and len(self._bids_list) > 0:  # will there be any match at all?
                existing_count = matching_key[0].get_count()
                diff = order.get_count() - existing_count
                if diff > 0:
                    # order will use up entirity of existing 
                    order.add_count(-existing_count)
                    # create trade object
                    trade = Trade(matching_key[0].get_price(), existing_count, order.get_timestamp())
                    self._completed_trades.append(trade)
                    # remove existing order
                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()
                    #check if there are any bids left at that price, if not
                    # remove key from dict + remove number from price list
                    if len(matching_key) == 0:
                        del self._bids[self._bids_list[-1]]
                        self._bids_list.pop(-1)
                    
                elif diff < 0:
                    # order will be used up entirely. 
                    matching_key[0].add_count(-order.get_count())
                    trade = Trade(matching_key[0].get_price(), order.get_count(), order.get_timestamp())
                    self._completed_trades.append(trade)
                    # order count to 0
                    order.add_count(-order.get_count())
                    # add order id
                    order.set_id(self._next_id)
                    self._order_ids.append(order.get_id())
                    self._next_id += 1
                else:  # diff == 0 case
                    #order used up, not added to book + matching order removed
                    order.add_count(-order.get_count())
                    trade = Trade(matching_key[0].get_price(), order.get_count(), order.get_timestamp())
                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()

                    if len(matching_key) == 0:
                        del self._bids[self._bids_list[-1]]
                        self._bids_list.pop(-1)
            else:  # add order to book
                self.add_ask(order)
                break
    
    def add_bid(self, order: Order):
        order.set_id(self._next_id)
        self._bids[order.get_price()].append(order)
        if order.get_price() not in self._bids_list:
            self._bids_list.add(order.get_price())
        self._order_ids.append(self._next_id)
        self._next_id += 1
    
    def add_ask(self, order: Order):
        order.set_id(self._next_id)
        self._asks[order.get_price()].append(order)
        if order.get_price() not in self._asks_list:
            self._asks_list.add(order.get_price())
        self._order_ids.append(self._next_id)
        self._next_id += 1

    def get_simple_bid_table(self):
        print(f'{'Bids':<6}')
        print(f"{'Order ID':<6} {'Price':<8} {'Quantity':<10} {'Timestamp/s':<8}")
        print('-' * 45)
        for price in reversed(self._bids_list):
            for order in self._bids[price]:
                print(f'{order.get_id():<6} {order.get_price():<8} {order.get_count():<10} {order.get_timestamp():<8}')
    
    def get_simple_ask_table(self):
        print(f'{'Asks':<6}')
        print(f"{'Order ID':<6} {'Price':<8} {'Quantity':<10} {'Timestamp/s':<8}")
        print('-' * 45)
        for price in self._asks_list:
            for order in self._asks[price]:
                print(f'{order.get_id():<6} {order.get_price():<8} {order.get_count():<10} {order.get_timestamp():<8}')

    def get_asks(self):
        return self._asks       
    
    def get_bids(self):
        return self._bids
    
    def get_trades(self):
        return self._completed_trades
