import pandas as pd
import plotly.graph_objects as go

# Read the original data file
df_original = pd.read_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\btcusdt_data_1h.csv', skiprows=1)

# Read the predicted price file
df_predicted = pd.read_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\predicted_price_btc_1h.csv')

# Convert timestamp columns to datetime with dayfirst=True
df_original['Open Timestamp'] = pd.to_datetime(df_original['Open Timestamp'], dayfirst=True)
df_original['Close Timestamp'] = pd.to_datetime(df_original['Close Timestamp'], dayfirst=True)
df_predicted['Close Timestamp'] = pd.to_datetime(df_predicted['Close Timestamp'])

# Extract required data for plotting
close_timestamps = df_original['Close Timestamp']
open_prices = df_original['Open Price']
high_prices = df_original['High Price']
low_prices = df_original['Low Price']
close_prices = df_original['Close Price']
predicted_timestamps = df_predicted['Close Timestamp']
predicted_prices = df_predicted['Predicted Price']  # Use 'Predicted Price' column instead of 'Close Price'

# Create the figure
fig = go.Figure()

# Add the candlestick trace from the original price data
fig.add_trace(go.Candlestick(
    x=close_timestamps,
    open=open_prices,
    high=high_prices,
    low=low_prices,
    close=close_prices,
    name='Original Price'
))

# Add the predicted closing price trace as a line
fig.add_trace(go.Scatter(
    x=predicted_timestamps,
    y=predicted_prices,
    name='Predicted Closing Price',
    line=dict(color='green')
))

# Configure the layout
fig.update_layout(
    title='Bitcoin Price',
    xaxis_title='Timestamp',
    yaxis_title='Price',
    showlegend=True,
)

# Show the plot
fig.show()

print("Latest data in df_original:")
print(df_original.tail(25))

print("Latest data in df_predicted:")
print(df_predicted.tail(25))
