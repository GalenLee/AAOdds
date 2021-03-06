import matplotlib.pyplot as plt
import numpy as np

# Create data
# x = np.random.rand(100).reshape(10,10)
x = np.linspace(0,1,100).reshape(10,10)

plt.subplots(facecolor=(.8, .8, .8), figsize=(8, 8))

# plt.clf()
plt.title('Pythonspot.com heatmap example')
plt.ylabel('y')
plt.xlabel('x')
plt.imshow(x, interpolation='none', vmin=0, vmax=1, aspect='equal')
#plt.figure(figsize=(5, 2.5))

ax = plt.gca()
ax.invert_yaxis()

# Major ticks
ax.set_xticks(np.arange(0, 10, 1))
ax.set_yticks(np.arange(0, 10, 1))

# Labels for major ticks
ax.set_xticklabels(np.arange(1, 11, 1))
ax.set_yticklabels(np.arange(1, 11, 1))

# Minor ticks
ax.set_xticks(np.arange(-.5, 10, 1), minor=True)
ax.set_yticks(np.arange(-.5, 10, 1), minor=True)

# Gridlines based on minor ticks
ax.grid(which='minor', color='w', linestyle='-', linewidth=1)

plt.show()