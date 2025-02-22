from ..utils.file_utils import read_json, write_json
from ..config import USER_DATA_PATH, PORTFOLIO_DATA_PATH
from ..models import PortfolioEntry
from .transaction_service import log_transaction
from ..utils.data_utils import get_stock_price

def buy_stock(username, ticker, quantity):
    """
    Buy stocks for a user.
    """
    users = read_json(USER_DATA_PATH)
    portfolio = read_json(PORTFOLIO_DATA_PATH)

    if username not in users:
        raise ValueError("User does not exist!")

    stock_price = get_stock_price(ticker)
    total_cost = stock_price * quantity

    if users[username]["balance"] >= total_cost:
        users[username]["balance"] -= total_cost

        # Add to portfolio
        if username not in portfolio:
            portfolio[username] = []
        portfolio[username].append(PortfolioEntry(username, ticker, quantity).__dict__)

        # Log transaction
        log_transaction(username, "buy", ticker, quantity, stock_price)

        # Save updated data
        write_json(USER_DATA_PATH, users)
        write_json(PORTFOLIO_DATA_PATH, portfolio)

        return {"message": "Stock purchased successfully!"}
    else:
        raise ValueError("Insufficient balance!")

def sell_stock(username, ticker, quantity):
    """
    Sell stocks for a user.
    """
    users = read_json(USER_DATA_PATH)
    portfolio = read_json(PORTFOLIO_DATA_PATH)

    if username not in users:
        raise ValueError("User does not exist!")

    if username not in portfolio:
        raise ValueError("User has no portfolio!")

    # Find the stock in the portfolio
    stock_found = False
    for entry in portfolio[username]:
        if entry["ticker"] == ticker:
            stock_found = True
            if entry["quantity"] < quantity:
                raise ValueError("Not enough shares to sell!")
            entry["quantity"] -= quantity
            if entry["quantity"] == 0:
                portfolio[username].remove(entry)  # Remove if quantity is zero
            break

    if not stock_found:
        raise ValueError("Stock not found in portfolio!")

    # Update user balance
    stock_price = get_stock_price(ticker)
    users[username]["balance"] += stock_price * quantity

    # Log transaction
    log_transaction(username, "sell", ticker, quantity, stock_price)

    # Save updated data
    write_json(USER_DATA_PATH, users)
    write_json(PORTFOLIO_DATA_PATH, portfolio)

    return {"message": "Stock sold successfully!"}