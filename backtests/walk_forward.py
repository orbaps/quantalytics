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

def walk_forward_split(df, train_years=5, test_years=1):
    """
    Implements a rolling walk-forward split.
    - Train window: train_years
    - Test window: test_years
    - Step size: 1 year
    """
    splits = []
    start = df.index.min()

    while True:
        train_start = start
        train_end = train_start + pd.DateOffset(years=train_years)
        test_end = train_end + pd.DateOffset(years=test_years)

        train = df.loc[train_start:train_end]
        test = df.loc[train_end:test_end]

        # Stop if no test data exists
        if len(test) == 0:
            break

        splits.append((train, test))
        
        # Increment step size (1 year)
        start += pd.DateOffset(years=1)
        
        # Prevent infinite loop if data is too small
        if start > df.index.max():
            break

    return splits

def run_walk_forward_backtest(df, name):
    print(f"\n--- Walk-Forward Validation: {name} ---")
    
    # Pre-calculate features (these are fixed per step in this methodology)
    df = df.copy()
    df['vol'] = rolling_volatility(df)
    df['regime'] = volatility_regimes(df['vol'])
    df = df.dropna()
    
    # Demonstration scale for 2024 snapshot (Quarterly splits)
    # This allows us to prove stability across segments of the year.
    splits = walk_forward_split(df, train_years=0, test_years=0) # Reset to use custom months
    
    # Implementing a custom monthly/quarterly split for the 2024 Evidence Table
    splits = []
    months = 3 # Quarterly steps
    for start_m in range(0, 9, months):
        train_end = df.index.min() + pd.DateOffset(months=start_m + 3)
        test_end = train_end + pd.DateOffset(months=months)
        
        train = df.loc[:train_end]
        test = df.loc[train_end:test_end]
        
        if len(test) > 100: # Ensure enough data
            splits.append((train, test))

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
    # Example for Gold
    try:
        df_gold = pd.read_csv('data/processed/XAUUSD_1H.csv', parse_dates=['Datetime']).set_index('Datetime')
        wf_results = run_walk_forward_backtest(df_gold, "GOLD - XAUUSD")
        print("\nWALK-FORWARD PERFORMANCE TABLE:")
        print(wf_results)
    except Exception as e:
        print(f"Error loading data: {e}")
