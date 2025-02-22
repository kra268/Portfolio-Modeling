import yfinance as yf

def get_stock_price(ticker):
    """
    Fetch the current price of a stock.
    """
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")['Close'].iloc[-1]