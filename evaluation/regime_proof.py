import pandas as pd
import numpy as np
import sys
import os

# Ensure local imports work
sys.path.append(os.getcwd())

from features.volatility import rolling_volatility
from features.regimes import volatility_regimes

def show_proof(asset_path, name):
    df = pd.read_csv(asset_path, parse_dates=['Datetime'])
    df.set_index('Datetime', inplace=True)
    df['vol'] = rolling_volatility(df)
    df['regime'] = volatility_regimes(df['vol'])
    
    print(f"\n{'='*40}")
    print(f"STATISTICAL PROOF ({name})")
    print(f"{'='*40}")
    print(f"Total Hours Analyzed: {len(df)}")
    print("\nRegime Distribution:")
    print(df['regime'].value_counts())
    
    ql = df['vol'].quantile(0.33)
    qh = df['vol'].quantile(0.66)
    
    print("\nVolatility Detection Thresholds:")
    print(f"LOW  < {ql:.6f}")
    print(f"MID  Range: [{ql:.6f} to {qh:.6f}]")
    print(f"HIGH > {qh:.6f}")
    
    print("\nSample Transition Data (Last 5 Rows):")
    print(df[['Close', 'vol', 'regime']].tail())
    print(f"{'='*40}")

if __name__ == "__main__":
    show_proof('data/processed/XAUUSD_1H.csv', 'GOLD - XAUUSD')
    show_proof('data/processed/XAGUSD_1H.csv', 'SILVER - XAGUSD')
