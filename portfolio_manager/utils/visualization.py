import matplotlib.pyplot as plt

def plot_portfolio_value(dates, values):
    """
    Plot portfolio value over time.
    """
    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.title("Portfolio Value Over Time")
    plt.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    plt.show()