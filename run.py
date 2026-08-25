from simulator import Simulator
from orders import Order
from agents import StandardAgent
from engine import LimitOrderBook

simulation = Simulator(num_agents = 100)

simulation.run(1000)

