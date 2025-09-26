import Global
from AddColumns import diffColumn

def statsCalc(column):
    meanVal = Global.marketDataFrame[column].mean()
    varVal  = Global.marketDataFrame[column].var()
    return meanVal, varVal

def statisticalAnalysis():
 
    if "diff" not in Global.marketDataFrame.columns:
        diffColumn()
    meanReturn, varReturn = statsCalc("diff")
    meanPrice, varPrice = statsCalc("c")

def sharpeRatio():
    if "diff" not in Global.marketDataFrame.columns:
        diffColumn()
    mean, var = statsCalc("diff")
    return mean/var