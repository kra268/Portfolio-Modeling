from dataclasses import dataclass

@dataclass
class User:
    username: str
    balance: float = 10000.0

@dataclass
class PortfolioEntry:
    username: str
    ticker: str
    quantity: int