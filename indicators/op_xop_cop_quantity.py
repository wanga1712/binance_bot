import pandas as pd
import numpy as np

# Read price data from CSV file
price_data = pd.read_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\btcusdt_data_1h.csv',
                         skiprows=1)

# Rename columns for convenience
price_data.rename(columns={'Open Timestamp': 'Open Timestamp', 'Open Price': 'Open Price', 'High Price': 'High Price',
                           'Low Price': 'Low Price', 'Close Timestamp': 'Close Timestamp',
                           'Close Price': 'Closing Price', 'Volume': 'Volume'}, inplace=True)

# Calculate Pivot Points
length = 10
n = price_data.shape[0]
ph = np.zeros(n)
pl = np.zeros(n)
max_price = 0.0
min_price = 0.0
max_x1 = 0
min_x1 = 0

last_pivot_type = ''  # Store the type of the last pivot (high or low)
last_pivot_value = np.nan  # Store the value of the last pivot

pivot_points = []  # Store the pivot points data as a list of dictionaries

for i in range(1, n - 1):
    high = price_data['High Price'][i]
    low = price_data['Low Price'][i]
    ph[i] = 1 if high > price_data['High Price'][i - 1] and high > price_data['High Price'][i + 1] else 0
    pl[i] = 1 if low < price_data['Low Price'][i - 1] and low < price_data['Low Price'][i + 1] else 0

    max_price = max(high, max_price)
    min_price = min(low, min_price)

    if max_price > price_data['High Price'][i - length:i].max():
        max_x1 = i - length

    if min_price < price_data['Low Price'][i - length:i].min():
        min_x1 = i - length

    if ph[i]:
        if last_pivot_type == 'low':
            pivot_points.append({'Pivot Type': 'Low', 'Pivot Value': last_pivot_value,
                                 'Date': price_data['Close Timestamp'][i - 1]})
        last_pivot_value = price_data['Closing Price'][i]
        last_pivot_type = 'high'

    elif pl[i]:
        if last_pivot_type == 'high':
            pivot_points.append({'Pivot Type': 'High', 'Pivot Value': last_pivot_value,
                                 'Date': price_data['Close Timestamp'][i - 1]})
        last_pivot_value = price_data['Closing Price'][i]
        last_pivot_type = 'low'

    max_price *= 0.997
    min_price *= 1.003

# Calculate OP, XOP, and COP using the pivot points
results = []

for i in range(len(pivot_points) - 3, -1, -1):
    a = pivot_points[i]['Pivot Value']
    b = pivot_points[i + 1]['Pivot Value']
    c = pivot_points[i + 2]['Pivot Value']

    op = round(((b - a) + c), 2)
    xop = round((0.618 * (b - a) + c), 2)
    cop = round((1.618 * (b - a) + c), 2)

    results.append({'Pivot Type': pivot_points[i]['Pivot Type'],
                    'Pivot Value (a)': round(a, 2),
                    'Date (a)': pivot_points[i]['Date'],
                    'Pivot Value (b)': round(b, 2),
                    'Date (b)': pivot_points[i + 1]['Date'],
                    'Pivot Value (c)': round(c, 2),
                    'Date (c)': pivot_points[i + 2]['Date'],
                    'OP': op,
                    'XOP': xop,
                    'COP': cop})

# Print the results in reverse order
for result in reversed(results):
    print(result['Pivot Type'] + ' (a):', result['Pivot Value (a)'], 'Date:', result['Date (a)'])
    print('Pivot (b):', result['Pivot Value (b)'], 'Date:', result['Date (b)'])
    print(result['Pivot Type'] + ' (c):', result['Pivot Value (c)'], 'Date:', result['Date (c)'])
    print('COP:', result['COP'], 'OP:', result['OP'], 'XOP:', result['XOP'])

# Create DataFrame from the results
df = pd.DataFrame(results)

# Reverse the DataFrame
df = df.iloc[::-1]

# Save DataFrame as CSV (overwriting the file)
df.to_csv(r'C:\Users\wangr\PycharmProjects\pythonProject2\data\requesst_btc_usdt\cop_op_xop_btc_1h.csv', index=False)
