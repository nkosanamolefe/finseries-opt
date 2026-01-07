from src import config
from src.loader import DataLoader
from src.preprocessor import Preprocessor
import matplotlib.pyplot as plt

def run_phase_1():
    # 1. Initialize Loader
    loader = DataLoader(
        tickers=config.TICKERS,
        start_date=config.START_DATE,
        end_date=config.END_DATE
    )

    # 2. Get Raw Prices (Extract/Load)
    prices = loader.get_data(force_refresh=True)
    print("\nRaw Prices Head:")
    print(prices.head())

    # 3. Compute Log Returns (Transform)
    log_returns = Preprocessor.compute_log_returns(prices)
    print("\nLog Returns Head:")
    print(log_returns.head())

    # 4. Statistical Validation (Applied Math)
    print("\nRunning Stationarity Tests...")
    for ticker in log_returns.columns:
        # Check raw price (Usually Non-Stationary)
        print(f"Testing Raw Prices for {ticker}:")
        Preprocessor.check_stationarity(prices[ticker])
        
        # Check returns (Usually Stationary)
        print(f"Testing Log Returns for {ticker}:")
        Preprocessor.check_stationarity(log_returns[ticker])

    # 5. Quick Visualization (Optional sanity check)
    plt.figure(figsize=(12, 6))
    plt.plot(log_returns)
    plt.title("JSE Top 40 Log Returns")
    plt.legend(log_returns.columns)
    plt.show()

if __name__ == "__main__":
    run_phase_1()