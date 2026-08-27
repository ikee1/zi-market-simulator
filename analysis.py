import numpy as np
import matplotlib.pyplot as plt

from orders import Trade

def get_prices(trades):
    return [trade.get_price() for trade in trades]

def get_quantities(trades):
    return [trade.get_quantity() for trade in trades]

def get_timestamps(trades):
    return [trade.get_timestamp() for trade in trades]

def calculate_returns(trades):
    prices = get_prices(trades)
    returns = []
    for i in range(len(prices)):
        r = (prices[i] - prices[i-1]) / prices[i-1] if i != 0 else 0
        returns.append(r)
    return returns

def calculate_log_returns(trades):
    prices = get_prices(trades)
    ln_returns = []
    for i in range(len(prices)):
        r = np.log(prices[i] / prices[i-1]) if i != 0 else 0
        ln_returns.append(r)
    return ln_returns

def calculate_volatility(trades):
    ln_returns = np.array(calculate_log_returns(trades))
    volatility = np.std(ln_returns)
    return volatility

def calculate_vwap(trades):
    """
    Returns a tuple (vwaps, timestamps), timestamps is a list of all times with a VWAP i.e. where at least a trade happened
    Plotting would look like VWAP against timestamps 
    """
    # for each timestamp (=1 second)
    times = get_timestamps(trades)
    prices = get_prices(trades)
    quants = get_quantities(trades)
    prod_list = [] # this will be a list of lists containing the price x quantity values for each timestamp
    quants_list = [] # this will be a list of lists containing the quantity for each trade per time stamp, so that each list
    times_list = [] # list of timestamps where actual trades occured, so which have a VWAP
    # can be summed over to get the total quantity for each timestamp
    for i in range(len(times)):
        if times[i] not in times_list:
            times_list.append(times[i])
        if i == 0:
            price_quant_prods = []
            total_quants = []
            price_quant_prods.append(quants[i] * prices[i])
            total_quants.append(quants[i])
        elif times[i] == times[i-1]:
            price_quant_prods.append(quants[i] * prices[i])
            total_quants.append(quants[i])
        else:
            prod_list.append(price_quant_prods)
            quants_list.append(total_quants)
            price_quant_prods = []
            total_quants = []
            price_quant_prods.append(quants[i] * prices[i])
            total_quants.append(quants[i])
    #appending the final list since no else to catch it
    prod_list.append(price_quant_prods)
    quants_list.append(total_quants)

    vwaps = []

    for i in range(len(times_list)):
        prod = sum(prod_list[i])
        quant = sum(quants_list[i])
        vwaps.append(prod / quant)

    return vwaps, times_list

