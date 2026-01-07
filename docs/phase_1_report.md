# Phase 1 Report: Infrastructure & Data Engineering

## Challenge: API Instability

**Issue:** The `yfinance` library recently updated its default behavior (v0.2.50+). It began automatically merging "Adjusted Close" calculations into the "Close" column.
**Impact:** This created ambiguity. For valid backtesting, we need:

1. **Raw Close:** To simulate Limit Orders and actual execution prices.
2. **Adjusted Close:** To calculate historical returns (accounting for dividends/splits).
**Solution:** I refactored `src/loader.py` to explicitly set `auto_adjust=False`. This forces the API to return the distinct columns, allowing the `DataLoader` class to selectively process the correct data stream.

## Challenge: I/O Latency

**Issue:** Loading 5 years of daily data for multiple tickers from CSV was becoming a bottleneck during repeated testing.
**Solution:** Implemented **Parquet** serialization using `pyarrow`.

* Maintained schema types (float64 vs object).
* Reduced disk usage via compression.
* Enabled the system to "Hot Load" data in < 50ms vs ~800ms for API fetches.

## Mathematical Validation

Executed Augmented Dickey-Fuller tests on JSE Top 40 constituents (NPN, FSR, AGL).

* **Result:** Raw prices failed to reject the Null Hypothesis (Non-Stationary).
* **Result:** Log-transformed returns consistently rejected the Null Hypothesis (p < 0.01).
* **Conclusion:** The preprocessing pipeline successfully transforms market data into a stationary format suitable for the ARIMA models planned in Phase 2.
