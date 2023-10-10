import pyswarms as ps
from pyswarms.utils.functions.single_obj import sphere
from pyswarms.utils.plotters import plot_surface
from pyswarms.utils.plotters.formatters import Mesher
import matplotlib.pyplot as plt

# Run optimizer
options = {'c1':0.5, 'c2':0.3, 'w':0.9}
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=2, options=options)

# Prepare position history
m = Mesher(func=sphere)
pos_history_3d = m.compute_history_3d(optimizer.pos_history)

# Plot!
plot_surface(pos_history_3d)
plt.show()

