import numpy as np

def rolling_volatility(df, window=30):
    """
    Computes rolling log-return volatility.
    """
    # Defensive mapping to handle case sensitivity
    data = df.copy()
    data.columns = [c.lower() for c in data.columns]
    
    log_ret = np.log(data["close"]).diff()
    vol = log_ret.rolling(window).std()
    return vol
