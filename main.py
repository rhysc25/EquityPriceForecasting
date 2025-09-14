from TechnicalAnalysis import backTesting
from DataDisplay import plotWithIndicators
from StatisticalAnalysis import statisticalAnalysis
from Exporting import exportDataframeSQL, checkForExistence, importFromSQL, exportDataframeCSV
from DataFetch import dataFetch
from Parameters import parameters
from MachineLearning import RandomForestAlgo
import Global

def importIfExists(parameters): # Needs a better way to check, takes too long
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

    # Machine Learning Classifiers
    RandomForestAlgo()

    # Export and Plot
    exportDataframeCSV()
    plotWithIndicators(parameters=parameters, show_ma = ["ema", "ma5", "ma15"], show_rsi=True)

    
if __name__ == "__main__":
   main(parameters)
