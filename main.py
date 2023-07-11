import os
import sys
from io import StringIO
from connected_api import get_account_balance, get_open_positions

# Get the current working directory
current_directory = os.getcwd()

# Construct the path to the config.py file
config_path = os.path.join(current_directory, 'config.py')

# Check if the config file exists
if os.path.exists(config_path):
    # Read the contents of the config.py file
    with open(config_path) as file:
        config_contents = file.read()

    # Create a dictionary to store the key-value pairs from the config file
    config_data = {}

    # Execute the config contents within the config_data dictionary
    exec(config_contents, config_data)

    # Retrieve the API key and secret key from the config_data dictionary
    api_key = config_data["API_KEYS"]["api_key"]
    secret_key = config_data["API_KEYS"]["secret_key"]

    # Suppress output using StringIO
    output = StringIO()
    sys.stdout = output

    # Get account balance
    account_balance, _ = get_account_balance(api_key, secret_key)
    print("=====================")  # Add dashes
    print("Account Balance:")
    if account_balance:
        for asset, balance in account_balance:
            print(f"Asset: {asset}, Balance: {balance}")
    else:
        print("No account balance data available.")
    print("=====================")  # Add dashes

    # Get open positions
    open_positions, _ = get_open_positions(api_key, secret_key)
    print("Open Positions:")
    if open_positions:
        for symbol, position_side, position_amt in open_positions:
            print(f"Symbol: {symbol}, Side: {position_side}, Size: {position_amt}")
    else:
        print("No open positions")
    print("=====================")  # Add dashes

    # Restore standard output
    sys.stdout = sys.__stdout__

    # Print the captured output
    print(output.getvalue())

else:
    print("Config file not found. Please make sure the 'config.py' file exists in the same directory as the script.")
