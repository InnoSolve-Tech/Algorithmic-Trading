"""
Functions for receiving modifying, reshaping and editing the data got from the HF servers.
"""
import pandas as pd
from urllib.request import urlopen
# import certifi
import json

_url = "https://financialmodelingprep.com/api/v3"



def fetchPastData() -> pd.DataFrame:
    url = ("https://financialmodelingprep.com/api/v3/historical-chart/5min/AAPL?from=2023-10-10&to=2023-08-10&apikey=YOUR_API_KEY'")
    print(get_jsonparsed_data(url))
    pass

def filterData(data : pd.DataFrame) -> pd.DataFrame:
    pass

def calcTools(data: pd.DataFrame) -> pd.DataFrame:
    pass

def displayTicks():
    pass

def someStrategy():
    # Strategy algorithm
    # open order
    # close order
    pass

def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

