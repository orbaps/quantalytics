import pandas as pd
import numpy as np
import sys
import os

# Ensure local imports work
sys.path.append(os.getcwd())

from strategies.baseline import baseline_strategy
from evaluation.metrics import strategy_returns

def verify_baseline(asset_path, name):
    df = pd.read_csv(asset_path, parse_dates=['Datetime'])
    df.set_index('Datetime', inplace=True)
    
    # Apply baseline (lookback=20)
    df_res = baseline_strategy(df, lookback=20)
    
    # Calculate returns
    df_res['strat_ret'] = strategy_returns(df_res)
    
    total_ret = np.exp(df_res['strat_ret'].sum())
    
    print(f"\n{'='*40}")
    print(f"BASELINE VALIDATION ({name})")
    print(f"{'='*40}")
    print(f"Total Cumulative Return Multiplier: {total_ret:.4f}")
    print("\nFinal Position Data:")
    print(df_res[['momentum', 'position', 'strat_ret']].tail())
    print(f"{'='*40}")

if __name__ == "__main__":
    verify_baseline('data/processed/XAUUSD_1H.csv', 'GOLD - XAUUSD')
    verify_baseline('data/processed/XAGUSD_1H.csv', 'SILVER - XAGUSD')
