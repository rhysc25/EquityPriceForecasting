import requests

from AlpacaKeys import Key, SecretKey

url = "https://data.alpaca.markets/v2/stocks/bars?symbols=SPY&timeframe=1D&start=2022-01-01T00%3A00%3A00Z&end=2023-01-01T00%3A00%3A00Z&limit=1000&adjustment=all&feed=sip&sort=asc"

headers = {
    "accept": "application/json",
    "APCA-API-KEY-ID": Key,
    "APCA-API-SECRET-KEY": SecretKey
}

response = requests.get(url, headers=headers)

print(response.text)
