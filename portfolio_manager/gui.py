import tkinter as tk
from tkinter import ttk, messagebox
from portfolio_manager.services.stock_service import buy_stock, sell_stock
from portfolio_manager.services.user_service import get_user, create_user
from portfolio_manager.services.portfolio_service import get_portfolio
from portfolio_manager.services.transaction_service import get_transactions
from portfolio_manager.utils.data_utils import get_stock_price
from portfolio_manager.utils.visualization import plot_portfolio_value
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Portfolio Manager")
        self.root.geometry("600x600")

        # Username Label and Entry
        self.username_label = ttk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Ticker Label and Entry
        self.ticker_label = ttk.Label(root, text="Stock Ticker:")
        self.ticker_label.grid(row=1, column=0, padx=10, pady=10)
        self.ticker_entry = ttk.Entry(root)
        self.ticker_entry.grid(row=1, column=1, padx=10, pady=10)

        # Real-Time Price Display
        self.price_label = ttk.Label(root, text="Current Price: -")
        self.price_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Quantity Label and Entry
        self.quantity_label = ttk.Label(root, text="Quantity:")
        self.quantity_label.grid(row=3, column=0, padx=10, pady=10)
        self.quantity_entry = ttk.Entry(root)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buy Button
        self.buy_button = ttk.Button(root, text="Buy Stock", command=self.buy_stock)
        self.buy_button.grid(row=4, column=0, padx=10, pady=10)

        # Sell Button
        self.sell_button = ttk.Button(root, text="Sell Stock", command=self.sell_stock)
        self.sell_button.grid(row=4, column=1, padx=10, pady=10)

        # Portfolio Display
        self.portfolio_text = tk.Text(root, height=10, width=50)
        self.portfolio_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Load Portfolio Button
        self.load_portfolio_button = ttk.Button(root, text="Load Portfolio", command=self.load_portfolio)
        self.load_portfolio_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Transaction History Display
        self.transaction_text = tk.Text(root, height=10, width=50)
        self.transaction_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Load Transactions Button
        self.load_transactions_button = ttk.Button(root, text="Load Transactions", command=self.load_transactions)
        self.load_transactions_button.grid(row=8, column=0, columnspan=2, pady=10)

        # Portfolio Value Chart
        self.figure, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        # Bind Ticker Entry to Update Price
        self.ticker_entry.bind("<FocusOut>", self.update_price)

    def update_price(self, event=None):
        """
        Update the real-time stock price display.
        """
        ticker = self.ticker_entry.get()
        if ticker:
            try:
                price = get_stock_price(ticker)
                self.price_label.config(text=f"Current Price: ${price:.2f}")
            except Exception as e:
                self.price_label.config(text="Current Price: -")
                messagebox.showerror("Error", f"Failed to fetch price for {ticker}: {str(e)}")
        else:
            self.price_label.config(text="Current Price: -")

    def buy_stock(self):
        """
        Handle the buy stock action.
        """
        username = self.username_entry.get()
        ticker = self.ticker_entry.get()
        quantity = self.quantity_entry.get()

        if not username or not ticker or not quantity:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            quantity = int(quantity)
            result = buy_stock(username, ticker, quantity)
            messagebox.showinfo("Success", result["message"])
            self.load_portfolio()  # Refresh portfolio display
            self.load_transactions()  # Refresh transaction history
            self.plot_portfolio_value(username)  # Update chart
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def sell_stock(self):
        """
        Handle the sell stock action.
        """
        username = self.username_entry.get()
        ticker = self.ticker_entry.get()
        quantity = self.quantity_entry.get()

        if not username or not ticker or not quantity:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            quantity = int(quantity)
            result = sell_stock(username, ticker, quantity)
            messagebox.showinfo("Success", result["message"])
            self.load_portfolio()  # Refresh portfolio display
            self.load_transactions()  # Refresh transaction history
            self.plot_portfolio_value(username)  # Update chart
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def load_portfolio(self):
        """
        Load and display the user's portfolio.
        """
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return

        portfolio = get_portfolio(username)
        self.portfolio_text.delete(1.0, tk.END)  # Clear previous content

        if not portfolio:
            self.portfolio_text.insert(tk.END, "No portfolio data found.")
        else:
            self.portfolio_text.insert(tk.END, "Your Portfolio:\n")
            total_value = 0
            for entry in portfolio:
                price = get_stock_price(entry["ticker"])
                value = price * entry["quantity"]
                total_value += value
                self.portfolio_text.insert(tk.END, f"{entry['ticker']}: {entry['quantity']} shares (${value:.2f})\n")
            self.portfolio_text.insert(tk.END, f"\nTotal Portfolio Value: ${total_value:.2f}")

    def load_transactions(self):
        """
        Load and display the user's transaction history.
        """
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return

        transactions = get_transactions(username)
        self.transaction_text.delete(1.0, tk.END)  # Clear previous content

        if not transactions:
            self.transaction_text.insert(tk.END, "No transactions found.")
        else:
            self.transaction_text.insert(tk.END, "Transaction History:\n")
            for transaction in transactions:
                self.transaction_text.insert(tk.END, f"{transaction['timestamp']} - {transaction['action'].upper()} {transaction['ticker']} ({transaction['quantity']} shares @ ${transaction['price']:.2f})\n")

    def plot_portfolio_value(self, username):
        """
        Plot the portfolio value over time.
        """
        transactions = get_transactions(username)
        if not transactions:
            return

        # Calculate portfolio value over time
        portfolio_value = []
        dates = []
        current_portfolio = {}

        for transaction in transactions:
            ticker = transaction["ticker"]
            quantity = transaction["quantity"]
            price = transaction["price"]
            action = transaction["action"]

            if ticker not in current_portfolio:
                current_portfolio[ticker] = 0

            if action == "buy":
                current_portfolio[ticker] += quantity
            elif action == "sell":
                current_portfolio[ticker] -= quantity

            # Calculate total portfolio value
            total_value = 0
            for t, q in current_portfolio.items():
                total_value += get_stock_price(t) * q

            portfolio_value.append(total_value)
            dates.append(transaction["timestamp"])

        # Plot the data
        self.ax.clear()
        self.ax.plot(dates, portfolio_value, marker="o")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Portfolio Value ($)")
        self.ax.set_title("Portfolio Value Over Time")
        self.ax.tick_params(axis="x", rotation=45)
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()