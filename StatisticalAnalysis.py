import Global

def diffColumn():
    Global.marketDataFrame["diff"] = Global.marketDataFrame["c"].diff()

def statsCalc(column):
    meanVal = Global.marketDataFrame[column].mean()
    varVal  = Global.marketDataFrame[column].var()
    return meanVal, varVal

def statisticalAnalysis():
 
    diffColumn()
    meanReturn, varReturn = statsCalc("diff")
    meanPrice, varPrice = statsCalc("c")

def sharpeRatio():
    mean, var = statsCalc("diff")
    return mean/var