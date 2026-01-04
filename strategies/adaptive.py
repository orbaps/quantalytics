import pandas as pd
import numpy as np
from features.momentum import momentum_signal

REGIME_PARAMS = {
    "LOW_VOL": {"lookback": 10, "size": 1.0},
    "MID_VOL": {"lookback": 20, "size": 0.75},
    "HIGH_VOL": {"lookback": 40, "size": 0.4},
}

def adaptive_strategy(df):
    """
    Implements a regime-adaptive momentum strategy.
    Parameters (lookback, size) are adjusted dynamically based on the current volatility regime.
    """
    df = df.copy()
    df["position"] = 0.0

    # Pre-calculate momentum signals for all required lookbacks to maintain alignment
    lookbacks = set(p["lookback"] for p in REGIME_PARAMS.values())
    mom_signals = {lb: momentum_signal(df, lookback=lb) for lb in lookbacks}

    # Map signals to regimes
    for regime, params in REGIME_PARAMS.items():
        # Select rows belonging to the current regime
        mask = df["regime"] == regime
        
        # Get the corresponding momentum signal
        mom = mom_signals[params["lookback"]]
        
        # Apply entry logic: Long if momentum > 0
        # Use the specific size parameter for the regime
        df.loc[mask & (mom > 0), "position"] = params["size"]

    return df
