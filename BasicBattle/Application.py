import numpy as np
import matplotlib.pyplot as plt
from Functions import calcProbDist
from Functions import calcCellWalk
from Functions import calcIteration
from matplotlib.animation import FuncAnimation

# Enter units.
attUnits = [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
defUnits = [4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

attUnits = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1]
defUnits = [4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

attUnits =  [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
defUnits =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

attUnits = [1,1,1,1,1]
defUnits = [1,1,1,1]

attUnits = [3,3,1,1,1,1,1]
defUnits = [4,2,2,2,2]




totAttUnits = len(attUnits) 
totDefUnits = len(defUnits)
totalUnits = totAttUnits + totDefUnits

# Calc dice roll distributions.
attDists = calcProbDist(attUnits)
defDists = calcProbDist(defUnits)

# Starting probability grid.  (0,0) for all attackers and defenders remaining.
probGrid = np.zeros((totalUnits, totalUnits), dtype = np.float64)
probGrid[0][0] = 1.0

# Calculate all iterations.
probGrids = []
probGrids.append(probGrid)
for i in range(totalUnits - 1): 
    probGrid = calcIteration(probGrid, totAttUnits, totDefUnits, attDists, defDists)
    probGrids.append(probGrid)

    # TODO: Calc dist and save


# Plot
x = probGrids[0]
#fig, ((ax1, ax), (ax2, ax3)) = plt.subplots(2, 2, facecolor=(.8, .8, .8), figsize=(15, 10))

plt.close('all')
fig = plt.figure(facecolor=(.8, .8, .8), figsize=(15, 10))
ax = plt.subplot(221)
ax2 = plt.subplot(222)
ax1 = plt.subplot(212)
plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=3.0)



N_points = 100000
n_bins = 20
x1 = np.random.randn(N_points)
ax1.hist(x1, bins=n_bins)


im = ax.imshow(x,  vmin=0, vmax=1)  #, aspect='equal'    interpolation='none',
ax.set_title('AA', fontsize = 18)
ax.set_xlabel('X', fontsize = 18)
ax.set_ylabel('Y', fontsize = 18)
ax.invert_yaxis()

# Major ticks
ax.set_xticks(np.arange(0, totalUnits, 1))
ax.set_yticks(np.arange(0, totalUnits, 1))

# Labels for major ticks
ax.set_xticklabels(np.arange(totAttUnits, totAttUnits - totalUnits, -1), fontsize = 18)
ax.set_yticklabels(np.arange(totDefUnits, totDefUnits - totalUnits, -1), fontsize = 18)
# ax.set_xticklabels(['1','2','c\n12'], fontsize = 18)

# Minor ticks
ax.set_xticks(np.arange(-.5, totalUnits, 1), minor = True)
ax.set_yticks(np.arange(-.5, totalUnits, 1), minor = True)

# Gridlines based on minor ticks
ax.grid(which='minor', color='w', linestyle='-', linewidth = 1)

def init():
    im.set_array(probGrids[0])
    return [im]

def animate(i):
    a = np.max(probGrids[i+1])
    b = probGrids[i+1].copy() / a
    im.set_array(b)
    return [im]

anim = FuncAnimation(fig, animate, frames = totalUnits-1, interval = 2000, blit = False, repeat = False)

plt.show()

