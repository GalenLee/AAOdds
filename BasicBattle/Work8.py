import numpy as np
from SimFunctions import XBattles

attUnits = [4,2,2]
defUnits = [3,3]

totAttUnits = len(attUnits) 
totDefUnits = len(defUnits)
totAttUnitsP1 = totAttUnits + 1
totDefUnitsP1 = totDefUnits + 1

countGrids = []
countGrid = np.zeros((totDefUnitsP1, totAttUnitsP1), dtype = np.int32)

XBattles(countGrids, countGrid, attUnits, defUnits, 10)
XBattles(None, countGrid, attUnits, defUnits, 100)

print(countGrids)
print(countGrid)