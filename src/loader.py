# src/loader.py
import yfinance as yf
import pandas as pd
from src import config

class DataLoader:
    """
    Responsible for fetching, saving, and loading financial time series data.
    """
    def __init__(self, tickers: list, start_date: str, end_date: str):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date

    def fetch_data(self) -> pd.DataFrame:
        """
        Fetches Adjusted Close prices from Yahoo Finance.

        NOTE ON YFINANCE API (2025 Update):
        Recent versions default to `auto_adjust=True`, which merges the adjustment
        into the 'Close' column and removes 'Adj Close'.
        We explicitly set `auto_adjust=False` to retrieve the specific 'Adj Close'
        column to ensure we are mathematically rigorous about dividends/splits.
        """
        print(f"Fetching data for: {self.tickers}")
        # download returns a MultiIndex DataFrame if multiple tickers
        raw_data = yf.download(
            self.tickers, 
            start=self.start_date, 
            end=self.end_date,
            progress=False,
            auto_adjust=False,
            multi_level_index=True # Ensures consistent format for 1 or many tickers
        )
        
        # Select specifically the Adjusted Close column
        # This accounts for Splits and Dividends (essential for accurate returns)
        data = raw_data['Adj Close']

        # Handle case where only 1 ticker is fetched (returns Series instead of DataFrame)
        if isinstance(data, pd.Series):
            data = data.to_frame()
            
        return data

    def get_data(self, force_refresh: bool = False) -> pd.DataFrame:
        """
        Orchestrator: Checks for local Parquet file first. 
        If not found or force_refresh is True, downloads from API.
        """
        file_path = config.RAW_DATA_DIR / "market_data.parquet"

        if file_path.exists() and not force_refresh:
            print("Loading data from local Parquet storage...")
            return pd.read_parquet(file_path)
        
        # Ingest
        df = self.fetch_data()
        
        # Save to Parquet
        df.to_parquet(file_path)
        print(f"Data saved to {file_path}")
        
        return df