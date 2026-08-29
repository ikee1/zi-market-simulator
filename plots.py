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
    ax.plot(prices / 100, "blue")
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
    ax.scatter(timestamps, prices / 100, label="trade prices", color="blue")
    ax.plot(all_times, fps / 100, label="fundamental price", color="red")
    ax.legend()

def plot_vwap(trades):
    vwaps, times = analysis.calculate_vwap(trades)

    fig, ax = plt.subplots()
    ax.set_xlabel("day")
    ax.set_ylabel("VWAP GBP")
    ax.set_title("VWAP")
    ax.plot(times, vwaps, "blue")

def plot_vwap_fundamental_overlay(trades, fps):
    vwaps, times = analysis.calculate_vwap(trades)
    fps_at_trade_times = [fps[t] for t in times]

    errors = np.array(vwaps) - np.array(fps_at_trade_times)

    print(np.mean(errors)/100)
    print(np.std(errors)/100)
    fig, ax = plt.subplots()
    ax.set_xlabel("day")
    ax.set_ylabel("VWAP GBP")
    ax.set_title("VWAP")
    ax.plot(np.arange(len(fps)), np.array(fps) / 100, "red")
    ax.plot(times, np.array(vwaps) / 100, "blue")

def plot_mad(stds, mads):
    fig, ax = plt.subplots()
    ax.set_title("Mean absolute deviation from fundamental price against standard deviation\nfor fundamental price interpretation of agents")
    ax.set_ylabel("MAD GBP")
    ax.set_xlabel("Fundamental price interpretation std GBP")
    ax.grid(True, which="both", axis="both", alpha=0.5)
    ax.plot(np.array(stds) / 100, np.array(mads) / 100, "blue")
