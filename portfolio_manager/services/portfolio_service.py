from ..utils.file_utils import read_json, write_json
from ..config import PORTFOLIO_DATA_PATH
from ..models import PortfolioEntry

def get_portfolio(username):
    """
    Retrieve portfolio data for a user.
    """
    portfolio = read_json(PORTFOLIO_DATA_PATH)
    return portfolio.get(username, [])

def add_to_portfolio(username, ticker, quantity):
    """
    Add a stock to the user's portfolio.
    """
    portfolio = read_json(PORTFOLIO_DATA_PATH)
    if username not in portfolio:
        portfolio[username] = []
    portfolio[username].append(PortfolioEntry(username, ticker, quantity).__dict__)
    write_json(PORTFOLIO_DATA_PATH, portfolio)