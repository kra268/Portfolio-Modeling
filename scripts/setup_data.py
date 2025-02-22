import sys
from pathlib import Path

# Add the project root directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from portfolio_manager.config import DATA_DIR, USER_DATA_PATH, PORTFOLIO_DATA_PATH
import os
import json

def initialize_data_files():
    """
    Initialize local data files for users and portfolios.
    """
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Initialize user data file (if it doesn't exist)
    if not os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, "w") as file:
            json.dump({}, file)  # Empty dictionary for user data
        print(f"Created user data file at {USER_DATA_PATH}")

    # Initialize portfolio data file (if it doesn't exist)
    if not os.path.exists(PORTFOLIO_DATA_PATH):
        with open(PORTFOLIO_DATA_PATH, "w") as file:
            json.dump({}, file)  # Empty dictionary for portfolio data
        print(f"Created portfolio data file at {PORTFOLIO_DATA_PATH}")

    print("Data files initialized successfully!")

if __name__ == "__main__":
    initialize_data_files()