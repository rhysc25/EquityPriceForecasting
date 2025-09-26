import requests
from AlpacaKeys import key, secretKey
import json
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

def backInTime(parameters):

    raw_ts = parameters["start"]
    decoded_ts = urllib.parse.unquote(raw_ts)
    dt = datetime.strptime(decoded_ts, "%Y-%m-%dT%H:%M:%SZ")
    new_dt = dt - timedelta(days=40)
    new_ts = new_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    encoded_ts = urllib.parse.quote(new_ts, safe='')

    return encoded_ts

def dataFetch(parameters):

    url = "https://data.alpaca.markets/v2/stocks/bars?symbols=" + parameters["symbols"]

    for parameter in parameters:
        if parameter == "symbols":
            pass
        elif parameters[parameter] == "":
            pass
        elif parameter == "start":
            start = backInTime(parameters=parameters)
            url = url + "&" + parameter + "=" + start
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

    marketDataFrame['t'] = pd.to_datetime(marketDataFrame['t']).dt.date

    shape = marketDataFrame.shape
    rowsTotal= shape[0]
    
    return marketDataFrame, rowsTotal

