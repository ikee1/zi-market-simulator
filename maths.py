
"""
Maths module with access to all the different 
functions required for the rest of the project
"""
import numpy as np
import random 
def box_muller():
    # creates two random variables u1 and u2 in [0,1]
    # and returns a standard normal value 
    u1 = 0
    u2 = 0
    while u1 < 1e-5:
        u1 = random.uniform(0,1)  # consider 1 - random.random()
    while u2 < 1e-5:
        u2 = random.uniform(0,1)
    z0 = np.sqrt(-2 * (np.log(u1))) * np.cos(2 * np.pi * u2)
    # z1 = np.sqrt(-2 * (np.log(u1))) * np.sin(2 * np.pi * u2)
    # this method produces two standard normal values, this could be
    # used later to reduce computation but for now just will do z0
    return z0
