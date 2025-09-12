from TechnicalAnalysis import backTesting
from DataDisplay import plotWithIndicators
from StatisticalAnalysis import statisticalAnalysis
from Exporting import exportDataframe, checkForExistence, importFromSQL
from Parameters import parameters

def importIfExists(parameters):
        if checkForExistence(parameters=parameters) == True:
            marketDataFrame = importFromSQL(parameters=parameters)
            print(marketDataFrame)

def main(parameters):
    
    importIfExists(parameters=parameters)
    statisticalAnalysis()
    backTesting()
    exportDataframe(parameters=parameters)
    plotWithIndicators(parameters=parameters, show_ma = ["ema", "ma5", "ma15"], show_rsi=True)

if __name__ == "__main__":
   main(parameters)
