from sortedcontainers import SortedList
from collections import deque, defaultdict

import numpy as np

from orders import Order, Trade

class LimitOrderBook:
    """
    Contains the mechanics and storage of the Limit Order Book
    """
    def __init__(self): 
        # default dictionary of price levels, each key (price level) is made up 
        # of a deque full of order objects
        self._bids = defaultdict(deque)
        self._asks = defaultdict(deque)

        # list of all available keys for bids/asks
        self._bids_list = SortedList([])
        self._asks_list = SortedList([]) 

        self._completed_trades = []
        self._next_id = 1
        self._order_ids = set()

    def process_order(self, order: Order):
        """
        Identifies an incoming order as a bid or an ask. Processes as required
        """
        if order.get_type() == True:
            new_trades = self.match_and_add_bid(order)
        else:
            new_trades = self.match_and_add_ask(order)
        return new_trades
    
    def match_and_add_bid(self, order: Order):
        """
        Match an incoming bid order against existing ask orders.

        The incoming bid is matched against the lowest priced asks first
        and then matched in terms of price-time priority. If there is any
        unfilled quantity in the incoming bid, it is added to the order
        book. Completed trades are recorded and returned.

        Parameters
        ----------
        order : Order
            The incoming bid order to match against the book

        Returns
        -------
        new_trades : list[Trade]
            Trades generated whilst matching the incoming order
        """
        new_trades = []
        while order.get_count() > 0 and order.get_id() not in self._order_ids:
            # no asks available, so bid cannot be matched
            if len(self._asks_list) == 0:
                self.add_bid(order)
                break
            
            # lowest (best) ask is always index 0 in _asks_list since the SortedList maintains
            # ascending order
            matching_key = self._asks[self._asks_list[0]]

            if order.get_price() >= self._asks_list[0]: 
                # difference between 
                # the oldest order on the key and the incoming order
                existing_count = matching_key[0].get_count()
                diff = order.get_count() - existing_count 

                if diff > 0: 
                    # incoming bid is larger, so the ask is completely filled
                    # and the remaining bid continues to be matched
                    order.add_count(-existing_count) 

                    # trade executes at the existing ask's price
                    trade = Trade(matching_key[0].get_price(), existing_count, order.get_timestamp())
                    self._completed_trades.append(trade)
                    new_trades.append(trade)
                    
                    # remove the existing ask from the book 
                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()

                    # if no more asks in the book at this price level,
                    # remove the key and remove the price from the 
                    # SortedList of ask prices
                    if len(matching_key) == 0:
                        del self._asks[self._asks_list[0]]
                        self._asks_list.pop(0)
                        
                elif diff < 0:
                    # existing order is bigger than incoming order, 
                    # order will never enter the book, it will be completely used up
                    matching_key[0].add_count(-order.get_count())

                    trade = Trade(matching_key[0].get_price(), order.get_count(), order.get_timestamp())
                    self._completed_trades.append(trade)
                    new_trades.append(trade)

                    order.add_count(-order.get_count())

                    # order ID is added to the list of IDs,
                    # this is to confirm it has completed processing
                    order.set_id(self._next_id)
                    self._order_ids.add(self._next_id)
                    self._next_id += 1
                else: 
                    # diff is 0, both orders are completely filled and so
                    # incoming bid must never enter book and existing ask 
                    # must be removed
                    order.add_count(-existing_count)

                    trade = Trade(matching_key[0].get_price(), existing_count, order.get_timestamp())
                    self._completed_trades.append(trade)
                    new_trades.append(trade)

                    order.set_id(self._next_id)
                    self._order_ids.add(self._next_id)
                    self._next_id += 1
                    
                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()

                    if len(matching_key) == 0:
                        del self._asks[self._asks_list[0]]
                        self._asks_list.pop(0)
            else:
                # best ask it too expensive so the incoming bid cannot match with it
                # and is instead added to the book
                self.add_bid(order)
                break
        return new_trades
    
    def match_and_add_ask(self, order: Order):
        """
        Match an incoming ask order against existing bid orders.

        The incoming ask is matched against the highest priced bids first
        and then matched in terms of price-time priority. If there is any
        unfilled quantity in the incoming ask, it is added to the order
        book. Completed trades are recorded and returned.

        Parameters
        ----------
        order : Order
            The incoming ask order to match against the book

        Returns
        -------
        new_trades : list[Trade]
            Trades generated whilst matching the incoming order
        """
        new_trades = []
        while order.get_count() > 0 and order.get_id() not in self._order_ids:
            # no bids available so ask cannot be matched
            if len(self._bids_list) == 0:
                self.add_ask(order)
                break

            # best bid is last element of SortedList _bids_list
            matching_key = self._bids[self._bids_list[-1]]
            if order.get_price() <= self._bids_list[-1]:
                # calculate difference in quantity between incoming ask and 
                # best existing bid
                existing_count = matching_key[0].get_count()
                diff = order.get_count() - existing_count

                if diff > 0:
                    # incoming ask order will use up entirity of the existing best bid
                    # ask will continue to be matched
                    order.add_count(-existing_count)

                    # trade executed at existing order's price
                    trade = Trade(matching_key[0].get_price(), existing_count, order.get_timestamp())
                    self._completed_trades.append(trade)
                    new_trades.append(trade)

                    # remove existing bid from the book
                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()

                    # check if there are any bids left at that price, if not
                    # remove key from dict + remove price from _bids_list
                    if len(matching_key) == 0:
                        del self._bids[self._bids_list[-1]]
                        self._bids_list.pop(-1)
                    
                elif diff < 0:
                    # incoming ask is smaller than existing best bid, it will
                    # be used up entirely and never added to the book
                    matching_key[0].add_count(-order.get_count())

                    trade = Trade(matching_key[0].get_price(), order.get_count(), order.get_timestamp())
                    self._completed_trades.append(trade)
                    new_trades.append(trade)

                    order.add_count(-order.get_count())

                    # order ID is added to the list of IDs,
                    # this is to confirm it has been processed
                    order.set_id(self._next_id)
                    self._order_ids.add(order.get_id())
                    self._next_id += 1

                else:
                    # diff is 0, incoming and existing orders are both fully used up
                    # and incoming order is never added to the book
                    order.add_count(-order.get_count())

                    trade = Trade(matching_key[0].get_price(), existing_count, order.get_timestamp())
                    self._completed_trades.append(trade)
                    new_trades.append(trade)

                    matching_key[0].add_count(-existing_count)
                    matching_key.popleft()

                    if len(matching_key) == 0:
                        del self._bids[self._bids_list[-1]]
                        self._bids_list.pop(-1)

            else:
                # incoming ask price is greater than the existing best bid, 
                # so they do not match and the incoming ask order is just 
                # added to book
                self.add_ask(order)
                break
        return new_trades
    
    def add_bid(self, order: Order):
        """Add bid to bid side of the LOB"""
        order.set_id(self._next_id)
        self._bids[order.get_price()].append(order)
        if order.get_price() not in self._bids_list:
            self._bids_list.add(order.get_price())
        self._order_ids.add(self._next_id)
        self._next_id += 1
    
    def add_ask(self, order: Order):
        """Add ask to ask side of the LOB"""
        order.set_id(self._next_id)
        self._asks[order.get_price()].append(order)
        if order.get_price() not in self._asks_list:
            self._asks_list.add(order.get_price())
        self._order_ids.add(self._next_id)
        self._next_id += 1

    def get_simple_bid_table(self):
        """Return a simple table containing the information on the current
        bids in the LOB"""
        print(f'{'Bids':<6}')
        print(f"{'Order ID':<6} {'Price':<8} {'Quantity':<10} {'Timestamp/s':<8}")
        print('-' * 45)
        for price in reversed(self._bids_list):
            for order in self._bids[price]:
                print(f'{order.get_id():<6} {order.get_price():<8} {order.get_count():<10} {order.get_timestamp():<8}')
    
    def get_simple_ask_table(self):
        """Return a simple table containing the information on the current
        asks in the LOB"""
        print(f'{'Asks':<6}')
        print(f"{'Order ID':<6} {'Price':<8} {'Quantity':<10} {'Timestamp/s':<8}")
        print('-' * 45)
        for price in self._asks_list:
            for order in self._asks[price]:
                print(f'{order.get_id():<6} {order.get_price():<8} {order.get_count():<10} {order.get_timestamp():<8}')

    def get_asks(self):
        """Return the asks dictionary"""
        return self._asks       
    
    def get_bids(self):
        """Return the bid dictionary"""
        return self._bids
    
    def get_trades(self):
        """Return the list of completed trades"""
        return self._completed_trades
    
    def get_ask_volume(self, N_levels):
        """
        Return the total volume of the top N_levels ask levels
        in the LOB.

        Parameters
        ----------
        N_levels : int or None
            The number of ask levels to consider. If None, all 
            available levels are considered

        Returns
        -------
        volume : int
            The total ask volume across the selected price levels
        """
        if N_levels is not None: 
            N = min(N_levels, len(self._asks_list))
        else:
            N = len(self._asks_list)
        tot_vols = []
        for i in range(N):
            price = self._asks_list[i]
            lvl_vols = []
            for order in self._asks[price]: 
                vol = order.get_count()
                lvl_vols.append(vol)
            tot_vols.append(np.sum(lvl_vols))
        volume = np.sum(tot_vols)
        return volume
    
    def get_bid_volume(self, N_levels):
        """
        Return the total volume of the top N_levels bid levels
        in the LOB.

        Parameters
        ----------
        N_levels : int or None
            The number of bid levels to consider. If None, all 
            available levels are considered

        Returns
        -------
        volume : int
            The total bid volume across the selected price levels
        """
        if N_levels is not None: 
            N = min(N_levels, len(self._bids_list))
        else:
            N = len(self._bids_list)
        tot_vols = []
        for i in range(N):
            price = self._bids_list[-i-1]
            lvl_vols = []
            for order in self._bids[price]:
                vol = order.get_count()
                lvl_vols.append(vol)
            tot_vols.append(np.sum(lvl_vols))
        volume = np.sum(tot_vols)
        return volume
        
    def get_midprice(self):
        """Return the midpoint between the best bid and best ask"""
        mid = (self._asks_list[0] + self._bids_list[-1]) / 2
        # mid = 2
        return mid