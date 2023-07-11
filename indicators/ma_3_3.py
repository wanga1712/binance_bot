import pandas as pd
import plotly.graph_objects as go
import numpy as np
from tqdm import tqdm

# Read the CSV file, skipping the first row
df = pd.read_csv('../data/requesst_btc_usdt/btcusdt_data_1h.csv', skiprows=[0])

# Rename the columns
df.columns = ['Open Timestamp', 'Open Price', 'High Price', 'Low Price', 'Close Timestamp', 'Close Price', 'Volume']

# Convert timestamp columns to datetime format
df['Open Timestamp'] = pd.to_datetime(df['Open Timestamp'], dayfirst=True, format='%d-%m-%Y %H:%M')
df['Close Timestamp'] = pd.to_datetime(df['Close Timestamp'], dayfirst=True, format='%d-%m-%Y %H:%M')

# Set 'Open Timestamp' as the index
df.set_index('Open Timestamp', inplace=True)

# Resample the DataFrame to have hourly frequency
df = df.resample('H').ffill()

# Calculate Moving Averages
ma_length_1 = 3
ma_offset_1 = 3

# Calculate the moving average using rolling() function
ma1 = df['Close Price'].rolling(window=ma_length_1).mean()

# Shift the moving average by the specified offset
ma1_shifted = ma1.shift(ma_offset_1)

# Select the last 1500 bars for visualization
df_last_1500 = df.tail(1500)
ma1_shifted_last_1500 = ma1_shifted.tail(1500)

# Combine the original data and the time-shifted moving average into a new DataFrame
df_combined = pd.concat([df_last_1500['Open Price'], df_last_1500['High Price'],
                         df_last_1500['Low Price'], df_last_1500['Close Price']], axis=1)
df_combined.columns = ['Open', 'High', 'Low', 'Close']

# Convert ma1_shifted_last_1500 to NumPy array and round the values to 2 decimal places
ma1_shifted_array = np.round(np.array(ma1_shifted_last_1500), 2)

# Create the candlestick trace
candlestick = go.Candlestick(
    x=df_last_1500.index,
    open=df_last_1500['Open Price'],
    high=df_last_1500['High Price'],
    low=df_last_1500['Low Price'],
    close=df_last_1500['Close Price'],
    name='Candlestick'
)

# Create the time-shifted moving average trace
ma_trace = go.Scatter(
    x=df_last_1500.index,
    y=ma1_shifted_array,
    mode='lines',
    name='Time-Shifted MA',
    line=dict(color='red')
)

# Create the layout
layout = go.Layout(
    title='Time-Shifted Moving Average',
    yaxis=dict(title='Price'),
    yaxis2=dict(title='MA', overlaying='y', side='right'),
    xaxis=dict(title='Date'),
)

# Create the figure
fig = go.Figure(data=[candlestick, ma_trace], layout=layout)

# Calculate the total iterations
total_iterations = len(df_last_1500)

# Perform the data processing with tqdm progress bar
with tqdm(total=total_iterations, desc='Processing data') as pbar:
    for i, row in df_last_1500.iterrows():
        # Perform data processing for each row
        # ...

        # Update the progress bar
        pbar.update(1)

# Display the figure
fig.show()
