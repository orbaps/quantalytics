import numpy as np
import pandas as pd

def rolling_volatility(df, window=30):
    """
    Calculates rolling standard deviation of log returns.
    """
    # Defensive check for column case
    close_col = 'Close' if 'Close' in df.columns else 'close'
    
    log_ret = np.log(df[close_col]).diff()
    vol = log_ret.rolling(window).std()
    return vol
