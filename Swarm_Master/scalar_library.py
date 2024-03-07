# This is a standard library for generating scalar functions and target functions for environment

import numpy as np
import settings as set
from scipy.optimize import minimize

def scalar_1(x, y):
    z = -(x**2 + y**2)
    return z

def scalar_2(x, y):
    z = np.cos(x/2) + np.sin(y/2)
    return z

def scalar_3(x, y):
    z = np.sinc((x/5)**2 + (y/5)**2) + np.sinc((x + 2)/5 + (y + 2)/5)/2
    return z

def scalar_4(x, y):
    z = x**2 + 20*np.sin(x) + y**2 - 20*np.sin(y)
    return z

def scalar_5(x, y):
    z = 1.5 * np.exp(-(x**2 + y**2) / (2*5**2)) + 0.01
    return z

def scalar_6(x, y):
    z = 1.5 * np.exp(-(x**2 + y**2) / (2*4.5**2))
    z += 0.5 * np.exp(-((x+10)**2 + (y+10)**2) / (2*4.5**2))
    z += 0.75 * np.exp(-((x-10)**2 + (y-10)**2) / (2*4.5**2))
    z += np.exp(-((x-10)**2 + (y+10)**2) / (2*4.5**2))
    z += 1.25 * np.exp(-((x+10)**2 + (y-10)**2) / (2*4.5**2))
    z += 0.01
    return z
