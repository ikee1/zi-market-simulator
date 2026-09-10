import random 

import numpy as np

def box_muller():
    """Generate a standard normal random variable using the Box-Muller transform"""
    u1 = 0
    u2 = 0

    while u1 < 1e-5:
        u1 = random.uniform(0,1) 
    while u2 < 1e-5:
        u2 = random.uniform(0,1)

    z0 = np.sqrt(-2 * (np.log(u1))) * np.cos(2 * np.pi * u2)

    return z0
