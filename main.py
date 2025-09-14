from TechnicalAnalysis import backTesting
from DataDisplay import plotWithIndicators
from StatisticalAnalysis import statisticalAnalysis
from Exporting import exportDataframeSQL, checkForExistence, importFromSQL, exportDataframeCSV
from Prediction import currentSimpleMovingAverage, currentExponentialMovingAverage
from Parameters import parameters
import Global
from DataFetch import dataFetch

def importIfExists(parameters):
    if checkForExistence(parameters=parameters) == True:
        Global.marketDataFrame, Global.rowsTotal = importFromSQL(parameters=parameters)
    else:
        Global.marketDataFrame, Global.rowsTotal = dataFetch(parameters=parameters)

def main(parameters):
    
    # Import from SQL Database
    importIfExists(parameters=parameters)
    exportDataframeSQL(parameters=parameters)
    
    # Fundamental and Statistical Analysis
    statisticalAnalysis()
    backTesting()

    # Export and Plot
    exportDataframeCSV()
    plotWithIndicators(parameters=parameters, show_ma = ["ema", "ma5", "ma15"], show_rsi=True)

    #print(currentExponentialMovingAverage(0.4,10)) DOESN'T WORK
    
if __name__ == "__main__":
   main(parameters)
