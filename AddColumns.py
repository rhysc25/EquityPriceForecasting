import Global
import numpy as np

def makeRSIColumn(periods):

    temp = np.zeros(Global.rowsTotal)

    for i in range(0, Global.rowsTotal):
        gainSum = 0
        lossSum = 0
        if i < periods:
            RSI = None
            temp[i] = RSI
        else:
            for j in range(0, periods):
                diff = Global.marketDataFrame["c"][i - j] - Global.marketDataFrame["c"][i - j - 1]
                if diff > 0:
                    gainSum += diff
                elif diff < 0:
                    lossSum -= diff
            if lossSum == 0:
                RSI = 100
            else:
                RS = gainSum/lossSum
                RSI = 100 - (100/(1 + RS))

            temp[i] = RSI

    Global.marketDataFrame["rsi"] = temp

def simpleMovingAverage(sampleNumber):
    num = str(sampleNumber)
    Global.marketDataFrame["ma" + num] = Global.marketDataFrame["c"].rolling(window=sampleNumber, min_periods=1).mean()

def exponentialMovingAverageExc(scaleFactor):

    temp = np.zeros(Global.rowsTotal)

    for i in range(0, Global.rowsTotal):
        if i == 0:
            temp[0] = Global.marketDataFrame["c"][0]
        else:
            temp[i] = Global.marketDataFrame["c"][i] * scaleFactor + temp[i-1] * (1 - scaleFactor)

    Global.marketDataFrame["ema"] = temp

def diffColumn():
    Global.marketDataFrame["diff"] = Global.marketDataFrame["c"].diff()