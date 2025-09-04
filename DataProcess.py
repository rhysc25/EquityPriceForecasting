import numpy as np
from GlobalVariables import marketDataFrame, rowsTotal

def dataProcess(parameters):

    timeArray = np.array([])
    vwArray = np.array([])

    for i in range(0,rowsTotal):
        timeArray = np.append(timeArray, marketDataFrame["t"][i])
        vwArray = np.append(vwArray, marketDataFrame["vw"][i])

    return timeArray, vwArray