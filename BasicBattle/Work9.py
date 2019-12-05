import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from Functions import runProbWalk
from SimFunctions import XBattles
from matplotlib.animation import FuncAnimation
from matplotlib import animation
from Functions import calcProbDist

attUnits = [4,3,3,3,1,1,1,1,1,1]
defUnits = [4,4,3,2,2,2,2,2]

attDists = calcProbDist(attUnits)
defDists = calcProbDist(defUnits)

totAttUnits = len(attUnits) 

plt.rcParams.update({'font.size': 20})

probsAtt = attDists[len(attDists)-1]
rectsAtt = plt.bar(np.arange(totAttUnits+1), probsAtt)
plt.xticks(np.arange(0, totAttUnits+1, 1))
plt.title('Hits')
plt.show()