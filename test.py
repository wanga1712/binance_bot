import pandas as pd
import datetime

# Read candlestick data from CSV file
candlestick_data = pd.read_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\btcusdt_data_1h.csv', skiprows=1)

# Read points data from CSV file
points_data = pd.read_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\cop_op_xop_btc_1h.csv')

# Convert 'Close Timestamp' column to datetime type
candlestick_data['Close Timestamp'] = pd.to_datetime(candlestick_data['Close Timestamp'], dayfirst=True)

# Extract the datetime values as a list
timestamp_values = candlestick_data['Close Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').values.tolist()

# Print the datetime values
for timestamp in timestamp_values:
    print(timestamp)
