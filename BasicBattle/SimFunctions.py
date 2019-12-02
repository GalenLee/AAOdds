import numpy as np

# One roll for Att and Def.
def OneStepRoll(attRem, defRem, attUnits, defUnits):
    while True:
        aHits = 0
        for i in range(attRem): aHits += 1 if np.random.uniform() <= attUnits[i]/6 else 0
        dHits = 0
        for i in range(defRem): dHits += 1 if np.random.uniform() <= defUnits[i]/6 else 0
        aHitsCap = defRem if aHits > defRem else aHits
        dHitsCap = attRem if dHits > attRem else dHits
        if aHitsCap > 0 or dHitsCap > 0:
            return (aHitsCap, dHitsCap)

# Save results.  Grid, remAtt, remDef, barAnim (flag).
def AddFramesToGrids(countGrids, countGrid, remAtt, remDef, frames, barAnim):
    if countGrids is not None: 
        for i in range(frames):
            countGrids.append((countGrid.copy(), remAtt, remDef, barAnim))

# One battle outcome.
def OneBattle(countResults, countGrid, attUnits, defUnits, frames):

    totAttUnits = len(attUnits) 
    totDefUnits = len(defUnits)

    remAtt = totAttUnits
    remDef = totDefUnits
    countGrid[totDefUnits - remDef][totAttUnits - remAtt] += 1
    AddFramesToGrids(countResults, countGrid, remAtt, remDef, frames, False)

    while remAtt > 0 and remDef > 0:
        results = OneStepRoll(remAtt, remDef, attUnits, defUnits)
        remAtt = remAtt - results[1]
        remDef = remDef - results[0]
        countGrid[totDefUnits - remDef][totAttUnits - remAtt] += 1
        AddFramesToGrids(countResults, countGrid, remAtt, remDef, frames, False)

    AddFramesToGrids(countResults, countGrid, remAtt, remDef, frames, True)   # True for Bar anim

# Multiple battles.
def XBattles(countGridsX, countResults, countGrid, attUnits, defUnits, iterations, frames):

    for i in range(iterations):
        OneBattle(countResults, countGrid, attUnits, defUnits, frames)

    if countGridsX is not None:
        countGridsX.append(countGrid.copy())