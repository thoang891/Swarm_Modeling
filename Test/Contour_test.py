import matplotlib.pyplot as plt
import numpy as np

delta = 0.025
x = np.arange(-10.0, 10.0, delta)
y = np.arange(-10.0, 10.0, delta)
X, Y = np.meshgrid(x, y)
# Z = (X**2 + Y**2)
Z = np.sin(X) * np.cos(Y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface with transparency
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.5)

# Add contour lines with transparency and labels
contour = ax.contour(X, Y, Z, zdir='z', offset=0, cmap='viridis', alpha=0.5)
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.1f')  # Label contour lines with Z value

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Plot with Contour Lines')

plt.show()