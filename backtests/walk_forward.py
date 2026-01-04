import pandas as pd
import numpy as np
import os
import sys

# Ensure local imports work
sys.path.append(os.getcwd())

from features.volatility import rolling_volatility
from features.regimes import volatility_regimes
from strategies.baseline import baseline_strategy
from strategies.adaptive import adaptive_strategy
from evaluation.metrics import strategy_returns, calculate_metrics

def walk_forward_split(df, train_months=3, test_months=3):
    """
    Implements a custom walk-forward split for short-term research snapshots.
    """
    splits = []
    start = df.index.min()
    
    # We step through the 2024 data in quarterly increments
    for i in range(0, 9, 3):
        train_end = start + pd.DateOffset(months=i + train_months)
        test_end = train_end + pd.DateOffset(months=test_months)
        
        train = df.loc[:train_end]
        test = df.loc[train_end:test_end]
        
        if len(test) > 100:
            splits.append((train, test))
            
    return splits

def run_walk_forward_backtest(df, name):
    print(f"\n--- Walk-Forward Validation: {name} ---")
    
    df = df.copy()
    df['vol'] = rolling_volatility(df)
    df['regime'] = volatility_regimes(df['vol'])
    df = df.dropna()
    
    splits = walk_forward_split(df)

    results = []
    for i, (train, test) in enumerate(splits):
        period_str = f"{test.index.min().date()} to {test.index.max().date()}"
        
        # Baseline
        df_base = baseline_strategy(test, lookback=20)
        df_base['strat_ret'] = strategy_returns(df_base)
        metrics_base = calculate_metrics(df_base['strat_ret'])
        
        # Adaptive
        df_adapt = adaptive_strategy(test)
        df_adapt['strat_ret'] = strategy_returns(df_adapt)
        metrics_adapt = calculate_metrics(df_adapt['strat_ret'])
        
        results.append({
            "period": period_str,
            "base_sharpe": metrics_base["Sharpe"],
            "base_dd": metrics_base["MaxDD"],
            "adapt_sharpe": metrics_adapt["Sharpe"],
            "adapt_dd": metrics_adapt["MaxDD"]
        })
        
    return pd.DataFrame(results)

if __name__ == "__main__":
    try:
        df_gold = pd.read_csv('data/processed/XAUUSD_1H.csv', parse_dates=['Datetime']).set_index('Datetime')
        wf_results = run_walk_forward_backtest(df_gold, "GOLD - XAUUSD")
        print("\nWALK-FORWARD PERFORMANCE TABLE:")
        print(wf_results)
    except Exception as e:
        print(f"Error: {e}")
