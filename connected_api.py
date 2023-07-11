from binance_f import RequestClient
import sys
from io import StringIO


def get_account_balance(api_key, secret_key):
    # Suppress output using StringIO
    output = StringIO()
    sys.stdout = output

    client = RequestClient(api_key=api_key, secret_key=secret_key, testnet=True)
    account_balance = client.get_balance()

    # Restore standard output
    sys.stdout = sys.__stdout__

    # Get the captured output
    output_data = output.getvalue().strip()  # Remove trailing newline

    # Process the account balance data
    if account_balance is not None:
        balances = []
        for balance in account_balance:
            if float(balance.balance) != 0:
                balances.append((balance.asset, balance.balance))
    else:
        balances = []

    # Return the balances and captured output
    return balances, output_data


def get_open_positions(api_key, secret_key):
    # Suppress output using StringIO
    output = StringIO()
    sys.stdout = output

    client = RequestClient(api_key=api_key, secret_key=secret_key, testnet=True)
    open_positions = client.get_position()

    # Restore standard output
    sys.stdout = sys.__stdout__

    # Get the captured output
    output_data = output.getvalue().strip()  # Remove trailing newline

    if open_positions is not None:
        # Process the open positions data
        positions = [(position.symbol, position.positionSide, position.positionAmt) for position in open_positions if
                     float(position.positionAmt) != 0]
    else:
        positions = []

    # Return the positions and captured output
    return positions, output_data
