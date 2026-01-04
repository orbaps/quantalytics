import pandas as pd
from features.momentum import momentum_signal

def baseline_strategy(df, lookback=20):
    """
    Baseline Baseline Momentum Strategy:
    - Long if momentum > 0
    - Flat if momentum <= 0
    - Fixed position size (1 unit)
    - No regime awareness
    """
    df = df.copy()
    # Ensure column casing for features module
    df.columns = [c.capitalize() if c.lower() == 'close' else c for c in df.columns]
    
    df["momentum"] = momentum_signal(df, lookback)
    df["position"] = 0
    df.loc[df["momentum"] > 0, "position"] = 1
    return df
