import pandas as pd

# Read candlestick data from CSV file
candlestick_data = pd.read_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\btcusdt_data_1h.csv', skiprows=1)

# Read points data from CSV file
points_data = pd.read_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\cop_op_xop_btc_1h.csv')

# Convert 'Close Timestamp' column to datetime type in candlestick_data
candlestick_data['Close Timestamp'] = pd.to_datetime(candlestick_data['Close Timestamp'], dayfirst=True)

# Iterate through the data array
reached_op_count = 0
reached_xop_count = 0
reached_cop_count = 0

for _, row in points_data.iterrows():
    timestamp_c = pd.to_datetime(row['Date (c)'], dayfirst=True)
    timestamp_a = pd.to_datetime(row['Date (a)'], dayfirst=True)

    # Filter the rows within the period from timestamp_c to timestamp_a in candlestick_data
    filtered_data = candlestick_data[
        (candlestick_data['Close Timestamp'] >= timestamp_c) &
        (candlestick_data['Close Timestamp'] < timestamp_a)
        ].copy()

    filtered_data.drop('Close Timestamp', axis=1, inplace=True)

    # Remove the 'Close Timestamp' column from filtered_data
    filtered_data.drop('Close Timestamp', axis=1, inplace=True)

    # Check if any of the calculated points (OP, XOP, COP) reached High Price or Low Price
    if any(filtered_data['High Price'] >= row['OP']) or any(filtered_data['Low Price'] <= row['OP']):
        reached_op_count += 1

    if any(filtered_data['High Price'] >= row['XOP']) or any(filtered_data['Low Price'] <= row['XOP']):
        reached_xop_count += 1

    if any(filtered_data['High Price'] >= row['COP']) or any(filtered_data['Low Price'] <= row['COP']):
        reached_cop_count += 1

# Print the results
print("Number of times OP reached High Price or Low Price:", reached_op_count)
print("Number of times XOP reached High Price or Low Price:", reached_xop_count)
print("Number of times COP reached High Price or Low Price:", reached_cop_count)
