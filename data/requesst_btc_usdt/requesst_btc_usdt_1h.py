import csv
import os
import requests
from datetime import datetime, timedelta
import time

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the path to the config file
config_path = os.path.join(current_directory, "..", "..", "config.py")


def get_api_keys():
    config_data = {}
    with open(config_path) as file:
        config_contents = file.read()
        exec(config_contents, config_data)
    api_keys = config_data["API_KEYS"]
    return api_keys


def convert_timestamp(timestamp):
    # Convert the timestamp from milliseconds to seconds
    timestamp /= 1000
    # Create a datetime object from the timestamp
    dt = datetime.fromtimestamp(timestamp)
    # Format the datetime object as per your requirement
    formatted_datetime = dt.strftime("%d-%m-%Y %H:%M")
    return formatted_datetime


def write_kline_data_to_csv(kline_data, symbol, interval):
    # Create the file name
    file_name = f"{symbol.lower()}_data_{interval}.csv"
    # Set the file path
    file_path = os.path.join(current_directory, file_name)

    # Open the file in write mode
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the symbol name as the header line
        writer.writerow([symbol])
        # Write the column headers
        writer.writerow(['Open Timestamp', 'Open Price', 'High Price', 'Low Price', 'Close Timestamp',
                         'Close Price', 'Volume'])

        # Write the kline data rows
        for kline in kline_data:
            open_timestamp = int(kline[0])
            close_timestamp = open_timestamp + (int(interval[:-1]) * 60 * 60 * 1000)
            formatted_open_datetime = convert_timestamp(open_timestamp)
            formatted_close_datetime = convert_timestamp(close_timestamp)
            open_price = kline[1]
            high_price = kline[2]
            low_price = kline[3]
            close_price = kline[4]
            volume = kline[5]

            writer.writerow([formatted_open_datetime, open_price, high_price, low_price,
                             formatted_close_datetime, close_price, volume])

    print(f"Kline data has been written to the file: {file_path}")


def get_kline_data(symbol, interval, start_time=None, end_time=None):
    api_keys = get_api_keys()
    api_key = api_keys["api_key"]

    if api_key is not None:
        # Set the endpoint URL
        endpoint = "https://fapi.binance.com/fapi/v1/klines"

        # Set the request parameters
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1500  # Maximum limit of 1500 bars
        }

        # Set the request headers
        headers = {
            "X-MBX-APIKEY": api_key
        }

        try:
            # Send the GET request
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()

            # Process the response
            kline_data = response.json()

            # Write the kline data to a CSV file
            write_kline_data_to_csv(kline_data, symbol, interval)

            return kline_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching kline data for {symbol}: {str(e)}")

    else:
        print("Error: API key not found")


def get_live_kline_data(symbol, interval):
    api_keys = get_api_keys()
    api_key = api_keys["api_key"]

    if api_key is not None:
        # Set the endpoint URL
        endpoint = "https://fapi.binance.com/fapi/v1/ticker/price"

        # Set the request parameters
        params = {
            "symbol": symbol
        }

        # Set the request headers
        headers = {
            "X-MBX-APIKEY": api_key
        }

        try:
            # Send the GET request
            response = requests.get(endpoint, params=params, headers=headers)
            response.raise_for_status()

            # Process the response
            price_data = response.json()

            # Create the live kline data from the price data
            open_price = price_data["price"]
            close_timestamp = datetime.now() + timedelta(hours=1)
            close_price = get_close_price(symbol, interval)
            live_kline_data = [[close_timestamp.timestamp() * 1000, open_price, open_price, open_price,
                                close_timestamp.timestamp() * 1000, close_price, 0]]

            return live_kline_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching live kline data for {symbol}: {str(e)}")

    else:
        print("Error: API key not found")


def get_close_price(symbol, interval):
    # Read the existing CSV file to get the close price of the latest candle
    file_name = f"{symbol.lower()}_data_{interval}.csv"
    file_path = os.path.join(current_directory, file_name)

    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            close_price = float(rows[-1][5])  # Get the close price of the last row
            return close_price
    except IOError:
        print(f"Error reading CSV file: {file_path}")
        return None


# Call the function to get kline data for a specific symbol
symbol = "BTCUSDT"
interval = "1h"
kline_data = get_kline_data(symbol, interval)

# Continuously fetch and update the live kline data
print("Waiting for data...")

while True:
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
    print(f"Waiting for data at {current_time}...")

    # Calculate the time for the next data point
    current_hour = datetime.now().hour
    next_hour = (current_hour + 1) % 24

    # Sleep until the next hour
    time_to_sleep = (60 - datetime.now().minute) * 60
    time_to_sleep += (60 - datetime.now().second)
    time_to_sleep += (60 - datetime.now().microsecond / 1000000)

    time_to_sleep += next_hour * 60 * 60

    # Sleep until the next hour
    time.sleep(time_to_sleep)

    # Fetch and write the live kline data
    live_kline_data = get_live_kline_data(symbol, interval)
    write_kline_data_to_csv(live_kline_data, symbol, interval)

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
    print(f"New data received and written to the file at {current_time}")
