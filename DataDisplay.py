import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from GlobalVariables import marketDataFrame, rowsTotal
import numpy as np

def dataProcess():

    timeArray = marketDataFrame["t"].to_numpy()
    vwArray   = marketDataFrame["vw"].to_numpy()

    return timeArray, vwArray

def dataDisplay(parameters):

    timeArray, vwArray = dataProcess()

    plt.clf()
    
    symbol = parameters["symbols"]
    title = symbol + " Price"
    print(title)
    plt.title(title)
    plt.xlabel('Time')

    if parameters["currency"] == "":
        units = "USD"
    else:
        units = parameters["currency"]

    plt.ylabel("Price /" + units)

    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(nbins=10))  # Limit to 10 ticks
    plt.xticks(rotation=45)

    plt.grid()
    plt.plot(timeArray, vwArray, label='Volume Weighted Average Price')
    plt.legend()
    plt.show()
