import requests
from AlpacaKeys import key, secretKey

parameters = {"symbols": "SPY", "timeframe": "1D", "start": "2022-01-01T00%3A00%3A00Z", "end": "2023-01-01T00%3A00%3A00Z", 
            "limit": "1000", "adjustment": "all", "asof": "", "feed": "sip", "currency": "", "page_token": "", "sort": "asc"}

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