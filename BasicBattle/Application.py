import numpy as np
import matplotlib.pyplot as plt
from Functions import calcProbDist
from Functions import calcCellWalk
from Functions import calcIteration
from matplotlib.animation import FuncAnimation
from matplotlib import animation

# Enter units.
attUnits =  [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
defUnits =  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
attUnits = [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
defUnits = [4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
attUnits = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1]
defUnits = [4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
attUnits = [1,1,1,1,1]
defUnits = [1,1,1,1]
attUnits = [3,3,1,1,1,1,1]
defUnits = [4,2,2,2,2]

attUnits = [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
defUnits = [4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

# Total units
totAttUnits = len(attUnits) 
totDefUnits = len(defUnits)
totAttUnitsP1 = totAttUnits + 1
totDefUnitsP1 = totDefUnits + 1
totalUnits = totAttUnits + totDefUnits

# Calc dice roll distributions.
attDists = calcProbDist(attUnits)
defDists = calcProbDist(defUnits)

# Starting probability grid.  Set [0,0] to 1.0. This is for all attackers and defenders remaining (i.e. prob 1.0).
probGrid = np.zeros((totDefUnitsP1, totAttUnitsP1), dtype = np.float64)
probGrid[0][0] = 1.0

# Calculate all iterations.
probGrids = []
probGrids.append(probGrid)
for i in range(totalUnits - 1): 
    probGrid = calcIteration(probGrid, totAttUnits, totDefUnits, attDists, defDists)
    probGrids.append(probGrid)

# Plot
pltSize = 10.0
fntSize = 12.0
titleSize = 16.0
fig = plt.figure(facecolor=(.8, .8, .8), figsize=(pltSize, pltSize * .7))
fig.suptitle('Axis and Allies Battle Outcomes', fontsize = titleSize)

grid = plt.GridSpec(4, 5, hspace = 0.6, wspace = 0.6)
axMain = fig.add_subplot(grid[1:, 0:-1])
axAtt = fig.add_subplot(grid[0, 0:-1], xticklabels=[], yticklabels=[])
axDef = fig.add_subplot(grid[1:, -1], xticklabels=[], yticklabels=[])
ax = fig.add_subplot(grid[0, -1])

# Attacker and Defender bar chart prep.
probsAtt = probGrids[totalUnits-1][-1]     # Last row
probAtt = sum(probsAtt) - probsAtt[-1]
probMaxAtt = max(probsAtt)
probsDef = probGrids[totalUnits-1][:,-1]  # Last column
probDef = sum(probsDef) - probsDef[-1]
probMaxDef = max(probsDef)
maxAttDef = max(probMaxAtt, probMaxDef)
bothLoseProd = probsAtt[-1]  # Same as probsDef[-1]

# Attacker Bar Plot
colorsAtt = [ (0.0, 0.25, 0.5) if (x > 0) else 'silver' for x in range(totAttUnitsP1)]
rectsAtt = axAtt.bar(np.arange(totAttUnits, -1, -1), np.flip(probsAtt), color = colorsAtt)
axAtt.set_ylabel("{:.1%}".format(probAtt), fontsize = titleSize)
axAtt.set_ylim([0, maxAttDef * 1.2])
axAtt.set_xticks(np.arange(0, totAttUnitsP1, 1))
#axAtt.set_xticklabels(np.arange(totAttUnits, -1, -1), fontsize = fntSize)
axAtt.set_xticks(np.arange(-.5, totAttUnitsP1 , 1), minor = True)

a = []
for x in range(totAttUnits + 1):
   a.append(str(totAttUnits - x) + '\n' + (str(attUnits[x]) if x<totAttUnits else ''))
axAtt.set_xticklabels(a, fontsize = fntSize)

# Defender Bar Plot
sideColors = [ (0.0, 0.25, 0.5) if (x > 0) else 'silver' for x in range(totDefUnitsP1)]
sideRects = axDef.barh(np.arange(totDefUnits, -1, -1), np.flip(probGrids[totalUnits-1][:,-1]), color = sideColors)
axDef.set_xlabel("{:.1%}".format(probDef), fontsize = titleSize)
axDef.set_xlim([0, maxAttDef * 1.2])
axDef.set_yticks(np.arange(0, totDefUnitsP1, 1))
#axDef.set_yticklabels(np.arange(totDefUnits, -1, -1), fontsize = fntSize)
axDef.set_yticks(np.arange(-.5, totDefUnitsP1 , 1), minor = True)

d = []
for x in range(totDefUnits + 1):
   d.append(str(totDefUnits - x) + ', ' + (str(defUnits[x]) if x<totDefUnits else '  '))
axDef.set_yticklabels(d, fontsize = fntSize)

# Zero left text area
ax.set_axis_off()
text = "{:.1%}".format(bothLoseProd)
ev = sum(np.flip(probsAtt) * range(0, totAttUnitsP1)) - sum(np.flip(probsDef) * range(0, totDefUnitsP1))
evText = "{:.1f}".format(ev)
txt = ax.text(0, .5, text + ' for 0\nEV = ' + evText, fontsize = titleSize)


# Main heat map for random walk.
im = axMain.imshow(probGrids[0],  vmin=0, vmax=1, cmap='Blues')
axMain.set_xlabel('Attacker Units Left / Hit Power', fontsize = titleSize)
axMain.set_ylabel('Defender Units Left / Hit Power', fontsize = titleSize)
axMain.invert_yaxis()
axMain.set_xticks(np.arange(0, totAttUnitsP1, 1))
axMain.set_yticks(np.arange(0, totDefUnitsP1 , 1))
axMain.set_xticklabels(np.arange(totAttUnits, -1, -1), fontsize = fntSize)  # 'a\nb\nc'
axMain.set_yticklabels(np.arange(totDefUnits, -1, -1), fontsize = fntSize)
axMain.set_xticks(np.arange(-.5, totAttUnitsP1 , 1), minor = True)
axMain.set_yticks(np.arange(-.5, totDefUnitsP1 , 1), minor = True)
axMain.grid(which='minor', color='grey', linestyle='-', linewidth = 1)


def init():
    im.set_array(probGrids[0])
    return [im]

def animate(i):

    # Main heat map (random walk)
    maxProb = np.max(probGrids[i])
    probs = probGrids[i].copy() / maxProb
    im.set_array(probs)

    # Show 
    probsAttAnim = probGrids[i][-1]     # Last row
    probAttAnim = sum(probsAttAnim) - probsAttAnim[-1]
    probsDefAnim = probGrids[i][:,-1]  # Last column
    probDefAnim = sum(probsDefAnim) - probsDefAnim[-1]
    bothLoseProdAnim = probsAttAnim[-1]  # Same as probsDef[-1]
    axAtt.set_ylabel("{:.1%}".format(probAttAnim), fontsize = titleSize)
    axDef.set_xlabel("{:.1%}".format(probDefAnim), fontsize = titleSize)

    textAnim = "{:.1%}".format(bothLoseProdAnim)
    evAnim = sum(np.flip(probsAttAnim) * range(0, totAttUnitsP1)) - sum(np.flip(probsDefAnim) * range(0, totDefUnitsP1))
    evTextAnim = "{:.1f}".format(evAnim)
    txt.set_text(textAnim + ' for 0\nEV = ' + evTextAnim)

    # Set attack outome bar heights
    for j in range(totAttUnits + 1):
        rectsAtt[j].set_height(probGrids[i][-1][totAttUnits-j])

    # Set defendar outcome bar heights
    for j in range(totDefUnits + 1):
        sideRects[j].set_width(probGrids[i][:,-1][totDefUnits-j])

    return [im]

anim = FuncAnimation(fig, animate, frames = totalUnits, interval = 1000, blit = False, repeat = False)

#plt.show()

anim.save('AAMedium1.gif', writer='pillow', fps = 1)
