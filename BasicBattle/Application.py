import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from Functions import runProbWalk
from SimFunctions import XBattles
from matplotlib.animation import FuncAnimation
from matplotlib import animation

# Inputs

#attUnits = [4,3,3,3,1,1,1,1,1,1]
#defUnits = [4,4,3,2,2,2,2,2]

attUnits = [4, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
defUnits = [4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

pauseFrames1 = 15
simXTicks = 10

pauseFrames2 = 30

animFrames = 8
animTicks = 20
pauseFrames3 = 30

pltSize = 10.0
fntSize = 9.0
titleSize = 16.0
saveGif = True
gifFile = 'temp.gif'

# Total units
totAttUnits = len(attUnits) 
totDefUnits = len(defUnits)
totAttUnitsP1 = totAttUnits + 1
totDefUnitsP1 = totDefUnits + 1
totalUnits = totAttUnits + totDefUnits

# Main probability calculations.
probGrids = runProbWalk(attUnits, defUnits)

# Simulations.
countGrid = np.zeros((totDefUnitsP1, totAttUnitsP1), dtype = np.int32)
countResults = []
countGridsX = []

#XBattles(None, countResults, countGrid, attUnits, defUnits, 1, 16)
#XBattles(None, countResults, countGrid, attUnits, defUnits, 1, 12)
XBattles(None, countResults, countGrid, attUnits, defUnits, 1, 5)
XBattles(None, countResults, countGrid, attUnits, defUnits, 1, 5)
XBattles(countGridsX, countResults, countGrid, attUnits, defUnits, 8, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 90, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 150, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 250, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 500, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 1500, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 2500, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 5000, 1)
XBattles(countGridsX, None, countGrid, attUnits, defUnits, 90000, 1)
#XBattles(countGridsX, None, countGrid, attUnits, defUnits, 900000, 1)
#XBattles(countGridsX, None, countGrid, attUnits, defUnits, 9000000, 1)

############
### Plot ###
############

fig = plt.figure(facecolor=(.9, .9, .9), figsize=(pltSize, pltSize * .7))
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
probsDef = probGrids[totalUnits-1][:,-1]   # Last column
probDef = sum(probsDef) - probsDef[-1]
probMaxDef = max(probsDef)
maxAttDef = max(probMaxAtt, probMaxDef)
bothLoseProd = probsAtt[-1]  # Same as probsDef[-1]

# Attacker Bar Plot
colorsAtt = [ (0.25, 0.5, 0.75) if (x > 0) else 'silver' for x in range(totAttUnitsP1)]
rectsAtt = axAtt.bar(np.arange(totAttUnits, -1, -1), np.flip(probsAtt), color = colorsAtt)
axAtt.set_ylabel("{:.1%}".format(probAtt), fontsize = titleSize)
axAtt.set_ylim([0, maxAttDef * 1.2])
axAtt.set_xticks(np.arange(0, totAttUnitsP1, 1))
axAtt.set_xticks(np.arange(-.5, totAttUnitsP1 , 1), minor = True)
axAttLabel = []
for x in range(totAttUnits + 1):
   axAttLabel.append(str(totAttUnits - x) + '\n' + (str(attUnits[x]) if x<totAttUnits else ''))
axAtt.set_xticklabels(axAttLabel, fontsize = fntSize)

# Defender Bar Plot
colorsDef = [ (0.25, 0.5, 0.75) if (x > 0) else 'silver' for x in range(totDefUnitsP1)]
rectsDef = axDef.barh(np.arange(totDefUnits, -1, -1), np.flip(probGrids[totalUnits-1][:,-1]), color = colorsDef)
axDef.set_xlabel("{:.1%}".format(probDef), fontsize = titleSize)
axDef.set_xlim([0, maxAttDef * 1.2])
axDef.set_yticks(np.arange(0, totDefUnitsP1, 1))
axDef.set_yticks(np.arange(-.5, totDefUnitsP1 , 1), minor = True)
axDefLabel = []
for x in range(totDefUnits + 1):
   axDefLabel.append(str(totDefUnits - x) + ', ' + (str(defUnits[x]) if x<totDefUnits else '  '))
axDef.set_yticklabels(axDefLabel, fontsize = fntSize)

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
axMain.set_xticklabels(np.arange(totAttUnits, -1, -1), fontsize = fntSize)
axMain.set_yticklabels(np.arange(totDefUnits, -1, -1), fontsize = fntSize)
axMain.set_xticks(np.arange(-.5, totAttUnitsP1 , 1), minor = True)
axMain.set_yticks(np.arange(-.5, totDefUnitsP1 , 1), minor = True)
axMain.grid(which='minor', color='grey', linestyle='-', linewidth = 1)

# Gets max value excluding 0, 0 cell.
# Used in scaling heat map data.
def MaxExcludeStartCell(gridCount):
    result = 0
    for d in range(totDefUnitsP1):
        for a in range(totAttUnitsP1):
            if d > 0 or a > 0:
                result = max(result, gridCount[d, a])
    return result

simStepFrames = len(countResults)
simXFrames = len(countGridsX)
lastCountResultsGrid = None if simStepFrames == 0 else countResults[simStepFrames-1][0]
maxCountForStepSim = 0 if simStepFrames == 0 else MaxExcludeStartCell(lastCountResultsGrid) * 1.25
maxCountForStepBar = 0 if simStepFrames == 0 else max(max(lastCountResultsGrid[-1]), max(lastCountResultsGrid[:,-1]))
factForStepBar = 0 if maxCountForStepBar == 0 else maxAttDef/maxCountForStepBar
rects = []

def init():
    im.set_array(probGrids[0])
    for j in range(totAttUnits + 1): rectsAtt[j].set_height(0)
    for j in range(totDefUnits + 1): rectsDef[j].set_width(0)
    fig.suptitle('', fontsize = titleSize)
    axAtt.set_ylabel('')
    axDef.set_xlabel('')
    txt.set_text('')
    return [im]

def animate(frame):

    # Clear any prior step rects
    for p in rects: p.remove()
    rects.clear()

    if frame < simStepFrames:

        # Main heat map (random walk)
        countResultsGrid = countResults[frame][0]
        im.set_array(countResultsGrid / maxCountForStepSim)
        txtSimulations = str(countResultsGrid[0][0])
        fig.suptitle('Axis and Allies - Simulations ' + txtSimulations, fontsize = titleSize)

        stepAttRem = countResults[frame][1]
        stepDefRem = countResults[frame][2]
        barAnim = countResults[frame][3]
        if barAnim:

            for j in range(totAttUnits + 1):
                rectsAtt[j].set_height(countResultsGrid[-1][totAttUnits-j] * factForStepBar)

            for j in range(totDefUnits + 1):
                rectsDef[j].set_width(countResultsGrid[:,-1][totDefUnits-j] * factForStepBar)

            if stepDefRem == 0:

                stepAttLocX = totAttUnits -stepAttRem - .4
                stepAttLocY = (countResultsGrid[-1][totAttUnits - stepAttRem] - 1) * factForStepBar
                axAttRect = patches.Rectangle(
                    (stepAttLocX, stepAttLocY), .8,  factForStepBar, 
                    linewidth = 3, edgecolor = 'r', facecolor = 'none')
                axAtt.add_patch(axAttRect)
                rects.append(axAttRect)

            if stepAttRem == 0:

                stepDefLocX = totDefUnits -stepDefRem - .4
                stepDefLocY = (countResultsGrid[:,-1][totDefUnits - stepDefRem] - 1) * factForStepBar
                axDefRect = patches.Rectangle(
                    (stepDefLocY, stepDefLocX), factForStepBar, .8, 
                    linewidth = 3, edgecolor = 'r', facecolor = 'none')
                axDef.add_patch(axDefRect)
                rects.append(axDefRect)

        else:
            stepAttLoc = totAttUnits -stepAttRem - .5
            stepDefLoc = totDefUnits - stepDefRem - .5
            rect = patches.Rectangle(
                (stepAttLoc, stepDefLoc), 1, 1, 
                linewidth = 3, edgecolor = 'r', facecolor = 'none')
            axMain.add_patch(rect)
            rects.append(rect)

    elif frame < simStepFrames + pauseFrames1:

        pass

    elif frame < simStepFrames + pauseFrames1 + simXFrames * simXTicks:

        idx = (frame - simStepFrames  - pauseFrames1) // simXTicks
        grid = countGridsX[idx]

        txtSimulations = str(grid[0][0])
        fig.suptitle('Axis and Allies - Simulations ' + txtSimulations, fontsize = titleSize)

        a = MaxExcludeStartCell(grid) * (1.25 if idx == 0 else 1)
        im.set_array(grid / a)

        pGrid = grid.copy()/grid[0][0]
        probsAttAnim = pGrid[-1]  
        probAttAnim = sum(probsAttAnim) - probsAttAnim[-1]
        probsDefAnim = pGrid[:,-1] 
        probDefAnim = sum(probsDefAnim) - probsDefAnim[-1]
        bothLoseProdAnim = probsAttAnim[-1] 
        axAtt.set_ylabel("{:.1%}".format(probAttAnim), fontsize = titleSize)
        axDef.set_xlabel("{:.1%}".format(probDefAnim), fontsize = titleSize)

        for j in range(totAttUnits + 1):
            rectsAtt[j].set_height(pGrid[-1][totAttUnits-j])

        for j in range(totDefUnits + 1):
            rectsDef[j].set_width(pGrid[:,-1][totDefUnits-j])

    elif frame < simStepFrames + pauseFrames1 + simXFrames * simXTicks + pauseFrames2:

        pass

    elif frame < simStepFrames + pauseFrames1 + simXFrames * simXTicks + pauseFrames2 + animFrames * animTicks:

        idx = (frame - simStepFrames  - pauseFrames1 - simXFrames * simXTicks - pauseFrames2) // animTicks

        fig.suptitle('Axis and Allies - Exact Outcomes', fontsize = titleSize)
        
        i = totalUnits - 1 if idx == animFrames - 1 else idx

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
        evAnimAtt = sum(np.flip(probsAttAnim) * range(0, totAttUnitsP1)) 
        evAnimDef = sum(np.flip(probsDefAnim) * range(0, totDefUnitsP1))
        evAnim = evAnimAtt - evAnimDef
        evTextAnim = "{:.1f}".format(evAnim)
        txt.set_text(textAnim + ' for 0\nEV = ' + evTextAnim)

        # Set attack outome bar heights
        for j in range(totAttUnits + 1):
            rectsAtt[j].set_height(probGrids[i][-1][totAttUnits-j])

        # Set defendar outcome bar heights
        for j in range(totDefUnits + 1):
            rectsDef[j].set_width(probGrids[i][:,-1][totDefUnits-j])

    else:

        pass

    return [im]

init()
anim = FuncAnimation(
    fig, animate,
    frames = simStepFrames + 
             pauseFrames1 + 
             simXFrames * simXTicks + 
             pauseFrames2 +
             animFrames * animTicks + 
             pauseFrames3, 
    interval = 1, blit = False, repeat = False)

if saveGif:
    anim.save(gifFile, writer='pillow', fps = 10)
else:
    plt.show()

print('Done')