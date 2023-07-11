import pandas as pd
import numpy as np

# Read the CSV file, skipping the first row
df = pd.read_csv('../data/requesst_btc_usdt/btcusdt_data_1h.csv', skiprows=[0])

# Rename the columns
df.columns = ['Open Timestamp', 'Open Price', 'High Price', 'Low Price', 'Close Timestamp', 'Close Price', 'Volume']

# Convert timestamp columns to datetime format
df['Open Timestamp'] = pd.to_datetime(df['Open Timestamp'], dayfirst=True, format='%d-%m-%Y %H:%M')
df['Close Timestamp'] = pd.to_datetime(df['Close Timestamp'], dayfirst=True, format='%d-%m-%Y %H:%M')

# Calculate the DiNapoli Oscillator Predictor
lookback_period = 20

# Calculate the DMA
dma = df['Close Price'].rolling(window=lookback_period, min_periods=int(lookback_period/2)).mean()

# Create an array to store the DMA values
dma_array = dma.dropna().to_numpy()

# Create a new DataFrame for XMA calculation
xma_df = pd.DataFrame({'DMA': dma_array})

# Calculate the XMA by shifting the DMA forward by N/2 periods
xma = xma_df['DMA'].shift(-int(lookback_period/2))

# Create a new array to store the XMA values
xma_values = np.full(len(df), np.nan)
xma_values[lookback_period-1:len(xma_values)] = xma.dropna().values

# Calculate the DiNapoli Oscillator Predictor using the XMA values
dinapoli_oscillator = df['Close Price'].iloc[lookback_period-1:] - xma_values[lookback_period-1:]

# Print the result
print("DiNapoli Oscillator Predictor:")
print(dinapoli_oscillator)

# Get the last known close price
last_close_price = df['Close Price'].iloc[-1]

# Calculate the predicted future price by adding the oscillator values to the last known close price
predicted_price = last_close_price + dinapoli_oscillator

# Print the predicted price
print("Predicted Future Price:")
print(predicted_price)

# Get the last known close price
last_close_price = df['Close Price'].iloc[-1]

# Calculate the predicted future price by adding the oscillator values to the last known close price
predicted_price = last_close_price + dinapoli_oscillator

# Create a new DataFrame to store the predicted prices and timestamps
predicted_df = pd.DataFrame({'Close Timestamp': df['Close Timestamp'].iloc[lookback_period-1:],
                             'Close Price': df['Close Price'].iloc[lookback_period-1:],
                             'Predicted Price': predicted_price})

# Save the predicted prices to a CSV file
predicted_df.to_csv('../data/requesst_btc_usdt/predicted_price_btc_1h.csv', index=False)
