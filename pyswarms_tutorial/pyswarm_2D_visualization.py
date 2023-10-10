# Import modules
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image

# Import PySwarms
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import (plot_cost_history, plot_contour, plot_surface)
from pyswarms.utils.plotters.formatters import Mesher

m = Mesher(func=fx.rosenbrock)

options = {'c1': 0.5, 'c2': 0.3, 'w':0.9} # arbitrary options
optimizer = ps.single.GlobalBestPSO(n_particles=50, dimensions=2, options=options)
cost, pos = optimizer.optimize(fx.rosenbrock, iters=100)

# Plot cost history
# plot_cost_history(cost_history=optimizer.cost_history)
# plt.show()

# 2D Animation
animation = plot_contour(pos_history=optimizer.pos_history, mesher=m, mark=(1,1))
animation.save('plot2.gif', writer='imagemagick', fps=8)
