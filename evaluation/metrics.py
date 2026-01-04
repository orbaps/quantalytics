import numpy as np

def strategy_returns(df):
    """
    Calculates strategy returns based on positions and log returns.
    Position is shifted by 1 to avoid look-ahead bias.
    """
    # Defensive mapping to handle case sensitivity
    data = df.copy()
    data.columns = [c.lower() for c in data.columns]
    
    log_ret = np.log(data["close"]).diff()
    # Shift position by 1: today's return is based on yesterday's position
    strat_ret = data["position"].shift(1) * log_ret
    return strat_ret
