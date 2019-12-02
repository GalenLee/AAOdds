import numpy as np

# Calculate probability distributions for Units in list.
#
# Example 4,3,1,1 will generate the following:
# List of arrays for outcomes [0 hits, 1 hit, 2 hits, 3 hits]
# 4       =>   [0.33333333  0.66666667]
# 4,3     =>   [0.16666667  0.50000000  0.33333333]
# 4,3,1   =>   [0.13888889  0.44444444  0.36111111  0.05555556]
def calcProbDist(units):

    results = []

    # Init outcome and add to results.
    outcome = np.array([1.0])
    results.append(outcome)

    for u in units:
        
        hitProb = u/6

        # loss dist.  Unit u misses.
        lossDist = outcome * (1 - hitProb)
        lossDist = np.append(lossDist, 0.0)

        # win dist.  Unit u hits.
        winDist = outcome * hitProb
        winDist = np.insert(winDist, 0, 0.0)

        outcome = lossDist + winDist
        results.append(outcome)

    return results


def calcCellWalk(sumGrid, cellProb, 
      totAttUnits, totDefUnits,
      attRem, defRem, 
      attProbDist, defProdDist):
    if cellProb > 0:
        factZeroHits = 1 - attProbDist[0] * defProdDist[0]
        for aHits in range(attRem + 1):
            for dHits in range (defRem + 1):
                if aHits > 0 or dHits > 0:
                    p = cellProb * attProbDist[aHits] * defProdDist[dHits] / factZeroHits
                    aHitsCap = defRem if aHits > defRem else aHits
                    dHitsCap = attRem if dHits > attRem else dHits
                    aIdx = totAttUnits - attRem + dHitsCap  # Notice att minus def hits
                    dIdx = totDefUnits - defRem + aHitsCap  # Notice def minus def hits
                    sumGrid[dIdx][aIdx] += p


def calcIteration(probGrid, totAttUnits, totDefUnits, attDists, defDists):

    # Copy probability grid working grid.
    sumGrid = probGrid.copy()

    # Zero out cells we are "walking" from.
    for aIdx in range(totAttUnits):
        for dIdx in range(totDefUnits):
            sumGrid[dIdx][aIdx] = 0

    # For each cell do a random walk.
    for aIdx in range(totAttUnits):
        for dIdx in range(totDefUnits):
            cellProb = probGrid[dIdx][aIdx]
            attRem = totAttUnits - aIdx
            defRem = totDefUnits - dIdx
            calcCellWalk(
                sumGrid, cellProb,
                totAttUnits, totDefUnits,
                attRem, defRem,
                attDists[attRem], defDists[defRem])

    return sumGrid


def runProbWalk(attUnits, defUnits):

    # Total units
    totAttUnits = len(attUnits) 
    totDefUnits = len(defUnits)
    totAttUnitsP1 = totAttUnits + 1
    totDefUnitsP1 = totDefUnits + 1
    totalUnits = totAttUnits + totDefUnits

    # Calc dice roll distributions.
    attDists = calcProbDist(attUnits)
    defDists = calcProbDist(defUnits)

    # Starting probability grid.  Set [0,0] to 1.0. 
    # This is for all attackers and defenders remaining (i.e. prob 1.0).
    # Notice grid[def][att].
    probGrid = np.zeros((totDefUnitsP1, totAttUnitsP1), dtype = np.float64)
    probGrid[0][0] = 1.0

    # Calculate all iterations.
    probGrids = []
    probGrids.append(probGrid)
    for i in range(totalUnits - 1): 
        probGrid = calcIteration(probGrid, totAttUnits, totDefUnits, attDists, defDists)
        probGrids.append(probGrid)

    return probGrids