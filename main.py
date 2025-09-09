from TechnicalAnalysis import backTesting
from DataDisplay import dataDisplay
from StatisticalAnalysis import statisticalAnalysis
from Parameters import parameters

def main(parameters):
    dataDisplay(parameters=parameters)
    statisticalAnalysis()
    backTesting()
    

if __name__ == "__main__":
   main(parameters)
