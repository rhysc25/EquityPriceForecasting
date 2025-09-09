from GlobalVariables import marketDataFrame, rowsTotal

def diffColumn():
    marketDataFrame["diff"] = marketDataFrame["c"].diff()

def statsCalc(column):
    meanVal = marketDataFrame[column].mean()
    varVal  = marketDataFrame[column].var()
    return meanVal, varVal

def statisticalAnalysis():
    diffColumn()
    meanReturn, varReturn = statsCalc("diff")
    meanPrice, varPrice = statsCalc("c")