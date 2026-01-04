import numpy as np
import pandas as pd

def bootstrap_sharpe_diff(ret_a, ret_b, n_iterations=1000):
    """
    Performs bootstrap resampling to determine the statistical significance
    of the difference between two Sharpe Ratios.
    """
    diffs = []
    n = len(ret_a)
    
    # Combined returns for joint sampling
    combined = pd.DataFrame({'a': ret_a, 'b': ret_b}).dropna()
    
    for _ in range(n_iterations):
        sample = combined.sample(n=len(combined), replace=True)
        
        # Calculate Sharpe for both (Assuming mean/std on sampled period)
        sa = sample['a'].mean() / sample['a'].std() if sample['a'].std() > 0 else 0
        sb = sample['b'].mean() / sample['b'].std() if sample['b'].std() > 0 else 0
        diffs.append(sb - sa)
        
    p_value = np.mean(np.array(diffs) <= 0)
    return np.mean(diffs), p_value

def regime_stability_test(df, returns_col='strat_ret'):
    """
    Tests if the strategy performance is stable across different volatility regimes.
    """
    summary = {}
    for regime in df['regime'].unique():
        if pd.isna(regime): continue
        
        regime_rets = df.loc[df['regime'] == regime, returns_col]
        summary[regime] = {
            "Mean_Ret": regime_rets.mean(),
            "Vol": regime_rets.std(),
            "Sharpe": regime_rets.mean() / regime_rets.std() if regime_rets.std() > 0 else 0
        }
    return pd.DataFrame(summary).T
