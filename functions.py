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
import pytz

_url = "https://financialmodelingprep.com/api/v3"



# Function to fetch past data from a financial API
def fetchPastData(mt5) -> pd.DataFrame:
    # Create an empty data frame to store the range bar data
    df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])
    # Get the current time
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime.now() - timedelta(hours=24)
    # get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
    rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, utc_from, 100)
    # create DataFrame out of the obtained data
    rates_frame = pd.DataFrame(rates)
    return rates_frame

# Function to filter and preprocess data
def filterData(data: pd.DataFrame) -> pd.DataFrame:
     # convert time in seconds into the datetime format
    data['timestamp']=pd.to_datetime(data['time'], unit='s')
    return data

# Function to calculate technical indicators
def calcTools(data: pd.DataFrame) -> pd.DataFrame:
    # Calculate additional technical indicators and add them to the DataFrame
    data['EMA_short'] = ta.trend.ema_indicator(data['close'], window=20)
    data['EMA_long'] = ta.trend.ema_indicator(data['close'], window=50)
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
    ax.plot(data['timestamp'].iloc[start_index:], data['EMA_long'].iloc[start_index:], label='EMA Long', linestyle='-', marker='o', color='orange')

    ax.legend()
    ax.set_title("Initial Plot of Last 50 Values with Technical Indicators")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Price")
    
    # Display the plot
    plt.show()

def ticksUpdate():
    pass


def someStrategy():
    # Strategy algorithm
    # open order
    # close order
    pass
