import pandas as pd
import numpy as np
import sys
import os

# Ensure local imports work
sys.path.append(os.getcwd())

from features.volatility import rolling_volatility
from features.regimes import volatility_regimes
from strategies.baseline import baseline_strategy
from strategies.adaptive import adaptive_strategy
from evaluation.metrics import strategy_returns, calculate_metrics
from evaluation.stats_tests import bootstrap_sharpe_diff, regime_stability_test

def run_comparison(asset_path, name):
    print(f"\n{'='*60}")
    print(f"PHASE 5 COMPARISON: {name}")
    print(f"{'='*60}")
    
    # 1. Load and Prepare Data
    df = pd.read_csv(asset_path, parse_dates=['Datetime'])
    df.set_index('Datetime', inplace=True)
    df['vol'] = rolling_volatility(df)
    df['regime'] = volatility_regimes(df['vol'])
    df = df.dropna()

    # 2. Execute Baseline
    df_base = baseline_strategy(df, lookback=20)
    df_base['strat_ret'] = strategy_returns(df_base)
    
    # 3. Execute Adaptive
    df_adapt = adaptive_strategy(df)
    df_adapt['strat_ret'] = strategy_returns(df_adapt)
    
    # 4. Compute Metrics
    metrics_base = calculate_metrics(df_base['strat_ret'])
    metrics_adapt = calculate_metrics(df_adapt['strat_ret'])
    
    comparison_df = pd.DataFrame({
        "Baseline": metrics_base,
        "Adaptive": metrics_adapt
    }).T
    
    print("\nPERFORMANCE COMPARISON TABLE:")
    print(comparison_df)
    
    # 5. Statistical Validation
    print("\nSTATISTICAL VALIDATION:")
    mean_diff, p_val = bootstrap_sharpe_diff(df_base['strat_ret'], df_adapt['strat_ret'])
    print(f"Bootstrap Mean Sharpe Diff (Adapt - Base): {mean_diff:.4f}")
    print(f"P-Value (Probability Adapt <= Base): {p_val:.4f}")
    
    if p_val < 0.05:
        print("RESULT: Statistical Significance achieved (p < 0.05).")
    else:
        print("RESULT: Difference is not statistically significant at 95% confidence.")

    # 6. Regime Stability
    print("\nPERFORMANCE BY REGIME (ADAPTIVE):")
    stability = regime_stability_test(df_adapt)
    print(stability)
    
    print(f"{'='*60}")

if __name__ == "__main__":
    # Run on Gold only for primary validation
    run_comparison('data/processed/XAUUSD_1H.csv', 'GOLD - XAUUSD')
    run_comparison('data/processed/XAGUSD_1H.csv', 'SILVER - XAGUSD')
