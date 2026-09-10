# Agent-Based Market Simulator
An agent-based continuous double auction market simulator investigating whether limit order book imbalance can predict short-term price movements.
## Overview
This project simulates a market populated by simple stochastic trading agents interacting through a continuous double auction. Agents form noisy perceptions of a stochastic fundamental price and submit limit orders around their perceived value. Orders are matched using price-time priority within a limit order book.

## Market Model
The simulation consists of the following:
- A limit order book containing bid and ask orders at different price levels,
- A continuous double auction matching system using price-time priority,
- Multiple stochastic trading agents, whose order prices are generated around a perceived fundamental price,
- A stochastic fundamental price which provides a reference value for agents' valuations.

The agents were inspired by zero-intelligence (ZI) market models, but incorporate knowledge of a fundamental price and place bids or asks based on this knowledge and therefore deviate from strictly the ZI model.

## Order book imbalance
At each observation point, order book imbalance is calculated using the total volume across the top $N$ bid and ask price levels:
$$
I = \frac{V_{bids} - V_{asks}}{V_{bids} + V_{asks}}
$$
where $V_{bids}$ and $V_{asks}$ are the total bid and ask volumes respectively.
A positive $I$ therefore indicates greater liquidity on the bid side and vice-versa.
The question this brought about, based on the paper The Price Impact of Order Book Events by Cont et. al., was whether this imbalance could be used to predict short term returns in my model. Just as it can in the real world. I wanted to investigate whether the agents in my model reproduce the necessary behaviour to utilise this as a trading strategy, despite having very low rationality.

I determined the ideal order book depth $N$ and the ideal horizon $h$ to produce the maximum correlation between imbalance over the $N$ levels and subsequent returns over the horizon.

### Book depth
I considered the range 1-10 levels at a constant horizon and sampling interval and achieved the following results:

<p align="center">
<img src="figures/order_book_depth_correlation.png" width="500">
</p>

Indicating clearly that $N = 3$ leads to the highest correlation.

### Horizon
I initially considered a large range of 5 through 50 steps (of increasing intervals) at constant $N$ and sampling interval, and found a peak at 5 so zoomed in further to 1-10 at intervals of 1 to achieve the following results

<p align="center">
<img src="figures/horizons_corr_zoomed_out.png" width="500">
<img src="figures/horizons_corr_zoomed_in.png" width="500">
</p>

Showing a clear peak at $h = 2$. So these were chosen as the optimal parameters.

The final strategy takes a long position when imbalance is positive, a short position when it is negative, and no position when it is 0. The position is held over a 2-step interval.

## Final Results
The final simulation used 30 simulations with 100,000 timesteps in each one, producing 1,212,971 total observations.

|Metric        |Imbalance Strategy  |Random Control  |
|:-------------|-------------------:|---------------:|
|Sharpe Ratio  |                0.10|         0.00081|
|Observations  |           1,212,971|       1,212,971| 

The Sharpe ratio is reported per 2-step simulation interval and is not annualised since the simulation timesteps do not have any mapping to the real world trading time.

The relatively large positive Sharpe ratio compared to the near-zero random control suggests that the simulated market does exhibit a non-random, short-term relationship between order book imbalance and subsequent returns.

## References
- Gode, Dhananjay K., and Shyam Sunder. “Allocative Efficiency of Markets with Zero-Intelligence Traders: Market as a Partial Substitute for Individual Rationality.” Journal of Political Economy 101, no. 1 (1993): 119–37. http://www.jstor.org/stable/2138676.
- Cont, Rama, Arseniy Kukanov, and Sasha Stoikov. "The price impact of order book events." Journal of financial econometrics 12, no. 1 (2014): 47-88.



