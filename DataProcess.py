from DataFetch import marketData, parameters
import json
import pandas as pd
import numpy as np

marketDataDict = json.loads(marketData)

"""
Sorts the close, high, low, number of trades, open, time stamp, volume of trades and the volume weighted price
into a pandas dataframe
"""


instrument = parameters["symbols"]
marketDataFrame = pd.DataFrame(marketDataDict["bars"][instrument])

shape = marketDataFrame.shape
rowsTotal, columnsTotal = shape[0], shape[1]

timeArray = np.array([])
vwArray = np.array([])

for i in range(0,rowsTotal):
    timeArray = np.append(timeArray, marketDataFrame["t"][i])
    vwArray = np.append(vwArray, marketDataFrame["vw"][i])
