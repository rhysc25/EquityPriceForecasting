import Global

def periodAggregation(trainingProportion):
    trainingPeriod = round(trainingProportion * Global.rowsTotal)

    trainingDataframe = Global.marketDataFrame.iloc[:trainingPeriod]
    validationDataframe = Global.marketDataFrame.iloc[trainingPeriod:]

    return trainingDataframe, validationDataframe

def currentRSI(periods):

    gainSum = 0
    lossSum = 0

    if periods > Global.rowsTotal - 1:
        Exception

    for i in range(0, periods):
        diff = Global.marketDataFrame["c"][Global.rowsTotal - i] - Global.marketDataFrame["c"][Global.rowsTotal - i - 1]
        if diff > 0:
            gainSum += diff
        elif diff < 0:
            lossSum -= diff
    if lossSum == 0:
        RSI = 100
    else:
        RS = gainSum/lossSum
        RSI = 100 - (100/(1 + RS))

    return RSI

def currentSimpleMovingAverage(sampleNumber):
    start = -sampleNumber
    return Global.marketDataFrame["c"][start:-1].mean()

def currentExponentialMovingAverage(scaleFactor, sampleNumber):

    temp = 0
    for i in range(1, sampleNumber):
        i = sampleNumber - i
        if i == sampleNumber - 1:
            temp += Global.marketDataFrame["c"][-i]
        else:
            temp = Global.marketDataFrame["c"][-i] * scaleFactor + temp * (1 - scaleFactor)
    
    return temp