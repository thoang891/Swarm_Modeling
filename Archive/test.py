import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image

import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import (plot_cost_history, plot_contour, plot_surface)
from pyswarms.utils.plotters.formatters import Mesher

m = Mesher(func=fx.sphere)

options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
n_particles = 50
dimensions = 2
optimizer = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=dimensions, options=options)
cost, pos = optimizer.optimize(fx.sphere, iters=100)

animation = plot_contour(pos_history=optimizer.pos_history, mesher=m, mark=(0,0))
animation.save('test_contour.gif', writer='imagemagick', fps=8)