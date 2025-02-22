import os

# Define paths for local data storage
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USER_DATA_PATH = os.path.join(DATA_DIR, "user_data.json")
PORTFOLIO_DATA_PATH = os.path.join(DATA_DIR, "portfolio_data.json")
TRANSACTIONS_PATH = os.path.join(DATA_DIR, "transactions.json")  # New

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)