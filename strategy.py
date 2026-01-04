import sys
import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy


# -----------------------------
# DATA LOADER (FIXED FOR YOUR CSV)
# -----------------------------
def load_and_prepare_data(csv_path):
    df = pd.read_csv(
        csv_path,
        header=None,
        names=["Date", "Time", "Open", "High", "Low", "Close", "Volume"]
    )

    df["Datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%Y.%m.%d %H:%M"
    )
    df.set_index("Datetime", inplace=True)

    df = df[["Open", "High", "Low", "Close", "Volume"]]

    # M1 -> M15
    # Use '15min' instead of '15T' to avoid deprecation warnings
    df = df.resample("15min").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()

    return df


# -----------------------------
# REAL STRATEGY
# -----------------------------
class VolatilityTrendStrategy(Strategy):
    risk_per_trade = 0.01
    atr_period = 14
    ema_fast = 50
    ema_slow = 200
    rsi_period = 14
    time_exit = 20

    def init(self):
        close = self.data.Close

        self.ema_fast_line = self.I(
            lambda x: pd.Series(x).ewm(span=self.ema_fast).mean().to_numpy(), close
        )
        self.ema_slow_line = self.I(
            lambda x: pd.Series(x).ewm(span=self.ema_slow).mean().to_numpy(), close
        )

        high, low = self.data.High, self.data.Low
        
        def calculate_atr(h, l, c):
            h, l, c = pd.Series(h), pd.Series(l), pd.Series(c)
            tr = pd.concat([
                h - l,
                (h - c.shift()).abs(),
                (l - c.shift()).abs()
            ], axis=1).max(axis=1)
            return tr.rolling(self.atr_period).mean().to_numpy()

        self.atr = self.I(calculate_atr, high, low, close)

        def calculate_rsi(x):
            s = pd.Series(x)
            diff = s.diff()
            gain = diff.clip(lower=0).rolling(self.rsi_period).mean()
            loss = diff.clip(upper=0).abs().rolling(self.rsi_period).mean()
            rs = gain / loss
            return (100 - (100 / (1 + rs))).to_numpy()

        self.rsi = self.I(calculate_rsi, close)

    def next(self):
        # Time-based exit
        if self.trades:
            trade = self.trades[-1]
            if len(self.data) - trade.entry_bar >= self.time_exit:
                trade.close()

        atr = self.atr[-1]
        if np.isnan(atr) or atr <= 0:
            return

        price = self.data.Close[-1]
        equity = self.equity

        # Risk-based position sizing
        # Refined formula: (equity * risk) / risk_per_unit_base
        # We use ATR directly as the risk distance. 
        # Price is high (2000+), so we divide by ATR to get quantity.
        risk_amount = equity * self.risk_per_trade
        risk_per_unit = 1.2 * atr # Same as SL distance
        size = risk_amount / risk_per_unit if risk_per_unit > 0 else 0

        if not self.position and size >= 1:
            # LONG
            # Relaxed EMA condition and Loosened RSI
            if self.ema_fast_line[-1] > self.ema_slow_line[-1] * 0.999 and 35 < self.rsi[-1] < 70:
                self.buy(
                    size=int(size),
                    sl=price - 1.2 * atr,
                    tp=price + 2.5 * atr
                )

            # SHORT
            # Relaxed EMA condition and Loosened RSI
            elif self.ema_fast_line[-1] < self.ema_slow_line[-1] * 1.001 and 30 < self.rsi[-1] < 65:
                self.sell(
                    size=int(size),
                    sl=price + 1.2 * atr,
                    tp=price - 2.5 * atr
                )


# -----------------------------
# UTILS & SPLITTING
# -----------------------------
def split_data(df, train_ratio=0.7):
    split_index = int(len(df) * train_ratio)
    train = df.iloc[:split_index]
    test = df.iloc[split_index:]
    return train, test


# -----------------------------
# BACKTEST RUNNER
# -----------------------------
def run_backtest(csv_path):
    print(f"\n--- Processing Asset: {csv_path} ---")
    data = load_and_prepare_data(csv_path)

    train_data, test_data = split_data(data)

    print("\n===== IN-SAMPLE (TRAIN) =====")
    bt_train = Backtest(
        train_data,
        VolatilityTrendStrategy,
        cash=100_000,
        commission=lambda size, price: min(2, 0.00002 * size * price)
    )
    stats_train = bt_train.run()
    print(stats_train)

    print("\n===== OUT-OF-SAMPLE (TEST) =====")
    bt_test = Backtest(
        test_data,
        VolatilityTrendStrategy,
        cash=100_000,
        commission=lambda size, price: min(2, 0.00002 * size * price)
    )
    stats_test = bt_test.run()
    print(stats_test)

    # bt_test.plot() # Commented out for headless environment


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python strategy.py <path_to_csv>")
    else:
        run_backtest(sys.argv[1])
