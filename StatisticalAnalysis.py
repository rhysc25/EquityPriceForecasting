import Global

def diffColumn():
    Global.marketDataFrame["diff"] = Global.marketDataFrame["c"].diff()

def statsCalc(column):
    meanVal = Global.marketDataFrame[column].mean()
    varVal  = Global.marketDataFrame[column].var()
    return meanVal, varVal

def statisticalAnalysis():
    print(Global.marketDataFrame)
    diffColumn()
    meanReturn, varReturn = statsCalc("diff")
    meanPrice, varPrice = statsCalc("c")