import numpy as np
import pandas as pd

def strategy_returns(df):
    """
    Calculates strategy returns based on positions and log returns.
    Position is shifted by 1 to avoid look-ahead bias.
    """
    data = df.copy()
    data.columns = [c.lower() for c in data.columns]
    
    log_ret = np.log(data["close"]).diff()
    strat_ret = data["position"].shift(1) * log_ret
    return strat_ret

def calculate_metrics(returns, risk_free_rate=0.0):
    """
    Computes professional risk-adjusted performance metrics.
    Assumes hourly returns.
    """
    if returns.empty or returns.isna().all():
        return {k: np.nan for k in ["Sharpe", "Sortino", "MaxDD", "CAGR", "TotalReturn"]}

    # Annualization factor (Hourly -> Yearly)
    # 24 hours * 252 trading days = 6048 (Approximation for crypto/metals often 24/7 or 24/5)
    # We'll use 252 * 24 = 6048 as a standard benchmark for institutional annualization
    ANN_FACTOR = 252 * 24

    # Total Return
    total_ret = np.exp(returns.sum()) - 1

    # Sharpe Ratio (Annualized)
    mean_ret = returns.mean() * ANN_FACTOR
    std_ret = returns.std() * np.sqrt(ANN_FACTOR)
    sharpe = (mean_ret - risk_free_rate) / std_ret if std_ret > 0 else 0

    # Sortino Ratio (Annualized)
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std() * np.sqrt(ANN_FACTOR)
    sortino = (mean_ret - risk_free_rate) / downside_std if downside_std > 0 else 0

    # Max Drawdown
    cum_ret = returns.cumsum().apply(np.exp)
    peak = cum_ret.cummax()
    drawdown = (cum_ret / peak) - 1
    max_dd = drawdown.min()

    # CAGR
    # Calculated based on the timeframe of the returns series
    days = (returns.index[-1] - returns.index[0]).days
    if days > 0:
        cagr = (total_ret + 1) ** (365 / days) - 1
    else:
        cagr = 0

    return {
        "Sharpe": round(sharpe, 3),
        "Sortino": round(sortino, 3),
        "MaxDD": f"{round(max_dd * 100, 2)}%",
        "CAGR": f"{round(cagr * 100, 2)}%",
        "TotalReturn": f"{round(total_ret * 100, 2)}%"
    }
