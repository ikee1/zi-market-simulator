import numpy as np
import matplotlib.pyplot as plt

import analysis

def plot_time_series(trades):
    prices = analysis.get_prices(trades)
    # needs vwap

def plot_time_series_event_driven(trades, num_agents, num_steps):
    prices = analysis.get_prices(trades)

    fig, ax = plt.subplots()

    ax.set_xlabel("trade")
    ax.set_ylabel("price GBP")
    ax.plot(prices, "blue")
    ax.set_title(f"{num_agents} Agents\n{num_steps} Timesteps")

def plot_returns(trades):
    returns = analysis.calculate_returns(trades)

    fig, ax = plt.subplots()
    ax.set_xlabel("trade")
    ax.set_ylabel("returns")
    ax.plot(returns, "blue")
    ax.set_title("returns")

def plot_log_returns(trades):
    returns = analysis.calculate_log_returns(trades)

    fig, ax = plt.subplots()
    ax.set_xlabel("trade")
    ax.set_ylabel("log returns")
    ax.plot(returns, "blue")
    ax.set_title("log returns")

def scatter_fundamental_price(trades, fps):
    prices = analysis.get_prices(trades)
    timestamps = analysis.get_timestamps(trades)
    all_times = np.arange(len(fps))

    fig, ax = plt.subplots()
    ax.set_ylabel("price GBP")
    ax.set_xlabel("time")
    ax.set_title("Trade prices over time, overlay of the evolving fundamental price\nevery 90 steps")
    ax.scatter(timestamps, prices, label="trade prices", color="blue")
    ax.plot(all_times, fps, label="fundamental price", color="red")
    ax.legend()
    