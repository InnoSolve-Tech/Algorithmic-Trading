"""
Functions for receiving modifying, reshaping and editing the data got from the HF servers.
"""
import pandas as pd
from urllib.request import urlopen
from datetime import datetime, timedelta
import requests
import json
import matplotlib.pyplot as plt
import ta

_url = "https://financialmodelingprep.com/api/v3"



# Function to fetch past data from a financial API
def fetchPastData() -> pd.DataFrame:
    # Get current datetime and the datetime 24 hours ago
    current_datetime = datetime.now()
    twenty_four_hours_ago = current_datetime - timedelta(hours=24)
    
    # Format datetimes as strings
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    twenty_four_hours_ago_str = twenty_four_hours_ago.strftime("%Y-%m-%d %H:%M:%S")
    
    # Construct API URL for historical data
    url = f"{_url}/historical-chart/1min/EURUSD?from={twenty_four_hours_ago_str}&to={current_datetime_str}&apikey=6bc8db76d4772b720e6f7decc2e48fb0"
    
    # Make a request to the API and normalize JSON response into a DataFrame
    response: requests.Response = requests.get(url)
    df = pd.json_normalize(response.json(), meta=["date", "open", "low", "high", "close"])
    return df

# Function to filter and preprocess data
def filterData(data: pd.DataFrame) -> pd.DataFrame:
    # Convert the "date" column to timestamp format and drop the original "date" column
    data["timestamp"] = data["date"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").timestamp())
    data.drop("date", axis=1, inplace=True)
    return data

# Function to calculate technical indicators
def calcTools(data: pd.DataFrame) -> pd.DataFrame:
    # Calculate additional technical indicators and add them to the DataFrame
    data['EMA_short'] = ta.trend.ema_indicator(data['close'], window=12)
    data['EMA_long'] = ta.trend.ema_indicator(data['close'], window=26)
    data['RSI'] = ta.momentum.rsi(data['close'], window=14)
    data['ATR'] = ta.volatility.average_true_range(data['high'], data['low'], data['close'], window=14)
    data['MACD'] = ta.trend.macd_diff(data['close'], window_slow=26, window_fast=12, window_sign=9)
    return data

# Function to display the last 50 values in a plot
def displayTicks(data: pd.DataFrame):
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    # Set up the initial plot
    fig, ax = plt.subplots()
    
    # Plot only the last 50 values
    start_index = max(0, len(data) - 50)
    ax.plot(data['timestamp'].iloc[start_index:], data['high'].iloc[start_index:], label='High', linestyle='-', marker='o', color='blue')
    ax.plot(data['timestamp'].iloc[start_index:], data['low'].iloc[start_index:], label='Low', linestyle='-', marker='o', color='green')
    ax.plot(data['timestamp'].iloc[start_index:], data['EMA_short'].iloc[start_index:], label='EMA Short', linestyle='-', marker='o', color='red')

    ax.legend()
    ax.set_title("Initial Plot of Last 50 Values with Technical Indicators")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Price")
    
    # Display the plot
    plt.show()



def someStrategy():
    # Strategy algorithm
    # open order
    # close order
    pass
