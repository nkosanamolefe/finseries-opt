import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller

class Preprocessor:
    """
    Handles mathematical transformations and statistical checks.
    """
    
    @staticmethod
    def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
        """
        Converts prices to Log Returns: R_t = ln(P_t / P_{t-1})
        """
        # np.log handles natural logarithm
        # .shift(1) moves prices down by 1 day to align P_{t-1} with P_t
        log_returns = np.log(prices / prices.shift(1))
        
        # Drop the first row which becomes NaN
        return log_returns.dropna()

    @staticmethod
    def check_stationarity(series: pd.Series, significance_level: float = 0.05):
        """
        Performs Augmented Dickey-Fuller test to check for stationarity.
        """
        print(f"--- ADF Test for {series.name} ---")
        
        # adfuller returns: adf_stat, pvalue, usedlag, nobs, crit_values...
        result = adfuller(series.dropna())
        
        p_value = result[1]
        is_stationary = p_value < significance_level
        
        print(f"ADF Statistic: {result[0]:.4f}")
        print(f"P-Value: {result[1]:.4f}")
        print(f"Stationary: {is_stationary}\n")
        
        return is_stationary