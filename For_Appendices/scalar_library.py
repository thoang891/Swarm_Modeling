# This is a standard library for generating scalar functions and target functions for environment

import numpy as np
import settings as set

def scalar_1(x, y, timestamp, center_x=0, center_y=0, current_time=0):
    amp = set.settings['amp']
    sigma = set.settings['sigma']
    timestamp = timestamp
    decay = set.settings['decay']
    z = (decay ** (1 + current_time - timestamp)) * amp * np.exp(-((x-center_x)**2 + (y-center_y)**2) / (2 * (sigma * (0.0001 + current_time - timestamp)) **2))
    return z
