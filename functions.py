"""
Functions for receiving modifying, reshaping and editing the data got from the HF servers.
"""
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import ta

_url = "https://financialmodelingprep.com/api/v3"



# Function to fetch past data from a financial API
def fetchPastData(mt5) -> pd.DataFrame:
    # Get the current time
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime.now() - timedelta(hours=24)
    # get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
    rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, utc_from, 60)
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
def displayTicks(data: pd.DataFrame, ax=None):
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
    if ax is None:
        # Set up the initial plot is ax is None.
        fig, ax = plt.subplots()

    # Plot only the last 50 values
    start_index = max(0, len(data) - 50)
    ax.clear()
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

def ticksUpdate(mt5, data: pd.DataFrame, ax=None):
    # Append the new row to the existing data
    utc_from = datetime.now()
    # Get new tick.
    new_row = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, utc_from, 1)
    # Convert the numpy array to a Dataframe.
    new_row = pd.DataFrame(new_row)
    # Convert timestamp to date.
    new_row = filterData(new_row)
    # Add new row to current data.
    data = pd.concat([data, new_row], ignore_index=True)
    # Display the new data.
    displayTicks(data, ax)


def someStrategy():
    # Strategy algorithm

    def someStrategy(data: pd.DataFrame, capital=10000):
    # Initialize positions
    position = 0  # 0 for no position, 1 for long, -1 for short

    # Iterate through the DataFrame starting from the second row
    for i in range(1, len(data)):
        # Check for EMA_short crossing over EMA_long (potential buy signal)
        if data['EMA_short'].iloc[i - 1] <= data['EMA_long'].iloc[i - 1] and data['EMA_short'].iloc[i] > data['EMA_long'].iloc[i] and position == 0:
            #or open order
            # Execute a buy order
            position = 1
            capital -= data['close'].iloc[i]  # Subtract the buy price from capital
            print(f"Buy: {data['timestamp'].iloc[i]}, Price: {data['close'].iloc[i]}, Capital: {capital}")

        # Check for EMA_short crossing under EMA_long (potential sell signal)
        elif data['EMA_short'].iloc[i - 1] >= data['EMA_long'].iloc[i - 1] and data['EMA_short'].iloc[i] < data['EMA_long'].iloc[i] and position == 1:
            # Execute a sell order
            position = 0
            capital += data['close'].iloc[i]  # Add the sell price to capital
            print(f"Sell: {data['timestamp'].iloc[i]}, Price: {data['close'].iloc[i]}, Capital: {capital}")

    # If there's an open position at the end, close it ......or close order
    if position == 1:
        capital += data['close'].iloc[-1]  # Add the last close price to capital
        print(f"Close Position: {data['timestamp'].iloc[-1]}, Price: {data['close'].iloc[-1]}, Capital: {capital}")
        
    pass
