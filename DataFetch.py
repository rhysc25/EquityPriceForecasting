import requests
from AlpacaKeys import key, secretKey
import json
import pandas as pd

def dataFetch(parameters):

    url = "https://data.alpaca.markets/v2/stocks/bars?symbols=" + parameters["symbols"]

    for parameter in parameters:
        if parameter == "symbols":
            pass
        elif parameters[parameter] == "":
            pass
        else:
            url = url + "&" + parameter + "=" + parameters[parameter]

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": key,
        "APCA-API-SECRET-KEY": secretKey
    }

    response = requests.get(url, headers=headers)
    marketData = response.text

    marketDataDict = json.loads(marketData)
    """
    Sorts the close, high, low, number of trades, open, time stamp, volume of trades and the volume weighted price
    into a pandas dataframe
    """
    instrument = parameters["symbols"]
    marketDataFrame = pd.DataFrame(marketDataDict["bars"][instrument])

    shape = marketDataFrame.shape
    rowsTotal= shape[0]

    return marketDataFrame, rowsTotal