import pandas as pd

def volatility_regimes(vol):
    """
    Classifies volatility into LOW / MID / HIGH regimes using quantiles.
    """
    q_low = vol.quantile(0.33)
    q_high = vol.quantile(0.66)

    regimes = pd.Series(index=vol.index, dtype="object")

    regimes[vol <= q_low] = "LOW_VOL"
    regimes[(vol > q_low) & (vol <= q_high)] = "MID_VOL"
    regimes[vol > q_high] = "HIGH_VOL"

    return regimes
