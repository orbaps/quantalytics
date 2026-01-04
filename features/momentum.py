import numpy as np

def momentum_signal(df, lookback=20):
    """
    Simple momentum signal based on cumulative log returns.
    """
    # Defensive mapping to handle case sensitivity
    data = df.copy()
    data.columns = [c.lower() for c in data.columns]
    
    log_ret = np.log(data["close"]).diff()
    momentum = log_ret.rolling(lookback).sum()
    return momentum
