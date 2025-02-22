from ..utils.file_utils import read_json, write_json
from ..config import TRANSACTIONS_PATH
from datetime import datetime

def log_transaction(username, action, ticker, quantity, price):
    """
    Log a transaction (buy/sell).
    """
    transactions = read_json(TRANSACTIONS_PATH)
    if username not in transactions:
        transactions[username] = []

    transaction = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "ticker": ticker,
        "quantity": quantity,
        "price": price,
    }
    transactions[username].append(transaction)
    write_json(TRANSACTIONS_PATH, transactions)

def get_transactions(username):
    """
    Retrieve all transactions for a user.
    """
    transactions = read_json(TRANSACTIONS_PATH)
    return transactions.get(username, [])