import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.getcwd())
from strategies.baseline import baseline_strategy
from evaluation.metrics import strategy_returns

def run_notebook_validation():
    df = pd.read_csv('data/processed/XAUUSD_1H.csv', parse_dates=['Datetime'])
    df.set_index('Datetime', inplace=True)
    
    # 1. Apply baseline strategy
    df_baseline = baseline_strategy(df, lookback=20)
    df_baseline['strat_ret'] = strategy_returns(df_baseline)
    
    # 2. Cumulative returns calculation
    df_baseline['cum_ret'] = df_baseline['strat_ret'].cumsum().apply(np.exp)
    
    # 3. Drawdown calculation
    drawdown = (df_baseline['cum_ret'] / df_baseline['cum_ret'].cummax() - 1)
    
    # 4. Plotting
    plt.figure(figsize=(15, 7))
    plt.plot(df_baseline.index, df_baseline['cum_ret'], label='Baseline Momentum (Lookback=20)', color='purple')
    plt.axhline(1, color='black', linestyle='--', alpha=0.5)
    plt.title('Baseline Strategy Performance (Control Group)')
    plt.ylabel('Cumulative Return Multiplier')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.savefig('notebooks/baseline_performance.png')
    
    print("Baseline Metrics (XAUUSD):")
    print(f"Final Multiplier: {df_baseline['cum_ret'].iloc[-1]:.4f}")
    print(f"Max Drawdown: {drawdown.min():.2%}")
    print("\nCommentary: Yes, this is mediocre.")

if __name__ == "__main__":
    run_notebook_validation()
