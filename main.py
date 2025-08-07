from DataFetch import dataFetch
from DataProcess import dataProcess
#from TechnicalAnalysis import 
from DataDisplay import dataDisplay

parameters = {"symbols": "SPY", "timeframe": "1D", "start": "2022-01-01T00%3A00%3A00Z", "end": "2023-01-01T00%3A00%3A00Z", 
            "limit": "1000", "adjustment": "all", "asof": "", "feed": "sip", "currency": "", "page_token": "", "sort": "asc"}

def main(parameters):
    marketData = dataFetch(parameters=parameters)
    timeArray, vwArray, marketDataFrame = dataProcess(marketData=marketData, parameters=parameters)
    dataDisplay(timeArray=timeArray, vwArray=vwArray, parameters=parameters)

if __name__ == "__main__":
   main(parameters)
