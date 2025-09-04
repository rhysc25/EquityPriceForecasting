from GlobalVariables import marketDataFrame, rowsTotal

def currentRSI(periods):

    gainSum = 0
    lossSum = 0

    if periods > rowsTotal - 1:
        Exception

    for i in range(0, periods):
        diff = marketDataFrame["c"][rowsTotal - i] - marketDataFrame["c"][rowsTotal - i - 1]
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

