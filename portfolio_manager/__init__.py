# Import key components to make them accessible at the package level
from .config import DATA_DIR, USER_DATA_PATH, PORTFOLIO_DATA_PATH
from .models import User, PortfolioEntry
from .services.stock_service import buy_stock
from .services.user_service import get_user, create_user
from .services.portfolio_service import get_portfolio, add_to_portfolio
from .utils.data_utils import get_stock_price
from .utils.visualization import plot_portfolio_value

# Package-level initialization (optional)
def initialize():
    """
    Initialize the package (e.g., ensure data directory exists).
    """
    import os
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Initialized data directory at {DATA_DIR}")

# Define what gets imported with `from portfolio_manager import *`
__all__ = [
    "User",
    "PortfolioEntry",
    "buy_stock",
    "get_user",
    "create_user",
    "get_portfolio",
    "add_to_portfolio",
    "get_stock_price",
    "plot_portfolio",
    "initialize",
]

# Optional: Run initialization when the package is imported
initialize()