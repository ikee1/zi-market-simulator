from simulator import Simulator
from orders import Order
from agents import StandardAgent
from engine import LimitOrderBook

simulation = Simulator(num_agents = 4)

simulation.run(5)

