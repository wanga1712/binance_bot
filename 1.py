from binance.cm_futures import CMFutures
from config import API_KEYS

api_key = API_KEYS["api_key"]
secret_key = API_KEYS["secret_key"]

client = CMFutures(key=api_key, secret=secret_key)

# Get account information
print(client.account())

# Get open positions
print(client.position_information())
