import sys
import os
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy


# -----------------------------
# DATA LOADER (FIXED FOR YOUR CSV)
# -----------------------------
def load_and_prepare_data(csv_path):
    """
    Loads pre-processed 1H research data.
    The data has already been resampled to 1H to eliminate microstructure noise.
    """
    df = pd.read_csv(csv_path)
    df["Datetime"] = pd.to_datetime(df["Datetime"])
    df.set_index("Datetime", inplace=True)
    
    # Ensure standard OHLCV columns exist
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    return df


# -----------------------------
# REAL STRATEGY
# -----------------------------
"""
# OLD STRATEGY DISABLED FOR RESEARCH PHASE 3
class VolatilityTrendStrategy(Strategy):
    ... (legacy code)
"""

if __name__ == "__main__":
    print("Regime Detection Module Active. Check notebooks/exploration.ipynb for validation.")
