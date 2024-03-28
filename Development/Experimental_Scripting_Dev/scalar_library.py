# This is a standard library for generating scalar functions and target functions for environment

import numpy as np
import settings as set


def scalar_1(x, y, center_x=0, center_y=0, current_time=0):
    amp = 1
    sig = 6
    timestamp = current_time
    decay = set.settings['decay']
    dt = set.settings['timestep']
    z = (decay ** (current_time-timestamp+dt)*dt) * amp * np.exp(-((x-center_x)**2 + (y-center_y)**2) / (2 * (sig * (1 + current_time)) **2))
    return z

def scalar_2(x, y, center_x=0, center_y=0, current_time=0):
    amp = 5
    sig = 5
    timestamp = current_time
    decay = set.settings['decay']
    dt = set.settings['timestep']
    z = (decay ** (current_time-timestamp+dt)*dt) * amp * 1.5 * np.exp(-((x-center_x)**2 + (y-center_x)**2) / (2*(sig * (1 + current_time))**2))
    z += (decay ** (current_time-timestamp+dt)*dt) * amp * 0.5 * np.exp(-((x-center_x+10)**2 + (y-center_y+10)**2) / (2*(sig * (1 + current_time))**2))
    z += (decay ** (current_time-timestamp+dt)*dt) * amp * 0.75 * np.exp(-((x-center_x-10)**2 + (y-center_y-10)**2) / (2*(sig * (1 + current_time))**2))
    z += (decay ** (current_time-timestamp+dt)*dt) * amp * np.exp(-((x-center_x-10)**2 + (y-center_y+10)**2) / (2*(sig * (1 + current_time))**2))
    z += (decay ** (current_time-timestamp+dt)*dt) * amp * 1.25 * np.exp(-((x-center_x+10)**2 + (y-center_y-10)**2) / (2*(sig * (1 + current_time))**2))
    return z

def scalar_3(x, y, center_x=0, center_y=0, current_time=0):
    amp = 10
    sig = 6
    timestamp = current_time
    decay = set.settings['decay']
    dt = set.settings['timestep']
    z = (decay ** (current_time-timestamp+dt)*dt) * amp * np.exp(-((x-center_x)**2 + (y-center_y)**2) / (2 * (sig * (1 + current_time)) **2))
    return z
