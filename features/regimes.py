import pandas as pd

def volatility_regimes(vol):
    """
    Classifies volatility into LOW, MID, and HIGH regimes based on 33rd and 66th quantiles.
    """
    q_low = vol.quantile(0.33)
    q_high = vol.quantile(0.66)

    regimes = pd.Series(index=vol.index, dtype="object")

    # Handle NaN values explicitly (will remain NaN/None)
    regimes[vol <= q_low] = "LOW_VOL"
    regimes[(vol > q_low) & (vol <= q_high)] = "MID_VOL"
    regimes[vol > q_high] = "HIGH_VOL"

    return regimes
