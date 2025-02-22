from setuptools import setup, find_packages

setup(
    name="stock_portfolio_manager",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask>=2.3.2",
        "pandas>=2.0.3",
        "yfinance>=0.2.18",
        "matplotlib>=3.7.1",
    ],
    entry_points={
        "console_scripts": [
            "portfolio-manager=portfolio_manager.app:main",
        ],
    },
)