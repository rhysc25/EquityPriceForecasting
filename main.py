from DataFetch import dataFetch
from DataProcess import dataProcess
from TechnicalAnalysis import movingAverageCrossover
from DataDisplay import dataDisplay
from Parameters import parameters

def main(parameters):
    timeArray, vwArray= dataProcess(parameters=parameters)
    buyTimes, sellTimes= movingAverageCrossover()
    dataDisplay(timeArray=timeArray, vwArray=vwArray, parameters=parameters)

if __name__ == "__main__":
   main(parameters)
