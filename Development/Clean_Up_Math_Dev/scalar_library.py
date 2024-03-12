# This is a standard library for generating scalar functions and target functions for environment

import numpy as np
import settings as set

def scalar_1(x, y, center_x=0, center_y=0):
    z = -((x-center_x)**2 + (y-center_y)**2)
    return z

def scalar_2(x, y, center_x=0, center_y=0):
    z = np.cos((x-center_x)/2) + np.sin((y-center_y)/2)
    return z

def scalar_3(x, y, center_x=0, center_y=0):
    z = np.sinc(((x-center_x)/5)**2 + ((y-center_y)/5)**2) + np.sinc(((x-center_x) + 2)/5 + ((y-center_y) + 2)/5)/2
    return z

def scalar_4(x, y, center_x=0, center_y=0):
    z = (x-center_x)**2 + 20*np.sin(x-center_x) + (y-center_y)**2 - 20*np.sin(y-center_y)
    return z

def scalar_5(x, y, center_x=0, center_y=0):
    amp = 1
    sig = 5
    z = amp * np.exp(-((x-center_x)**2 + (y-center_y)**2) / (2 * sig **2))
    return z

def scalar_6(x, y, center_x=0, center_y=0):
    z = 1.5 * np.exp(-((x-center_x)**2 + (y-center_x)**2) / (2*4.5**2))
    z += 0.5 * np.exp(-((x-center_x+10)**2 + (y-center_y+10)**2) / (2*4.5**2))
    z += 0.75 * np.exp(-((x-center_x-10)**2 + (y-center_y-10)**2) / (2*4.5**2))
    z += np.exp(-((x-center_x-10)**2 + (y-center_y+10)**2) / (2*4.5**2))
    z += 1.25 * np.exp(-((x-center_x+10)**2 + (y-center_y-10)**2) / (2*4.5**2))
    return z
