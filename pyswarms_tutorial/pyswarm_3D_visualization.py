# Import modules
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Image, display, HTML

# Import PySwarms
import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import (plot_cost_history, plot_contour, plot_surface)
from pyswarms.utils.plotters.formatters import (Mesher, Designer)

m = Mesher(func=fx.sphere)
d = Designer(limits=[(-1,1), (-1,1), (-0.1,1)], label=['x-axis', 'y-axis', 'z-axis'])

options = {'c1': 0.5, 'c2': 0.3, 'w':0.9} # arbitrary options
optimizer = ps.single.GlobalBestPSO(n_particles=50, dimensions=2, options=options)
cost, pos = optimizer.optimize(fx.sphere, iters=100)

# 3D Animation
# Prepare position history

pos_history_3d = m.compute_history_3d(optimizer.pos_history)
animation3d = plot_surface(pos_history=pos_history_3d, mesher=m, designer=d, mark=(0,0,0))
plt.show()
# animation3d.save('plot3d.gif', writer='imagemagick', fps=8)
# Image(url='plot3d.gif')
#animation3d.save('pso_animation.gif', writer='imagemagick', fps=10)
# Display the animation directly

# Having issues getting a 3D animation to display