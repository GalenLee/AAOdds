import matplotlib.pyplot as plt
import numpy as np

# Create data
x = np.random.rand(100)
y = np.random.rand(100)
print(x)

# Create heatmap
heatmap, xedges, yedges = np.histogram2d(x, y, bins=(10,10))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

fig, ax = plt.subplots(facecolor=(.8, .8, .8))
#ax.grid(linewidth='0.5', color='white')

# Plot heatmap
plt.clf()
plt.title('Pythonspot.com heatmap example')
plt.ylabel('y')
plt.xlabel('x')
plt.imshow(heatmap, extent=extent)


ax = plt.gca()
ax.grid(color='w', linestyle='-', linewidth=2)

plt.show()