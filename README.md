# Quantalytics: Regime-Adaptive Volatility-Aware Momentum Strategy

A research-grade quantitative system designed for Gold (**XAUUSD**) and Silver (**XAGUSD**). This project moves beyond retail-grade "M1 noise" to focus on high-fidelity institutional timeframes (1H) and regime-adaptive logic.

### 🧪 Research Question
> **"Does adapting momentum strategies to market volatility regimes significantly improve risk-adjusted returns in precious metals compared to static momentum strategies?"**

---

## 🚀 Quick Start

### 1. Setup Environment
```bash
python -m venv venv
# Activate venv (Windows)
.\venv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
```

### 2. Research-Grade Preprocessing (M1 -> 1H)
We strictly avoid M1 data to eliminate microstructure noise and artificial backtest inflation.
```bash
python data/processed/preprocess.py
```

### 3. Run Strategy
```bash
python strategy.py
```

---

## 🛠️ Data Methodology
- **Raw Data**: 1-minute (M1) institutional feeds.
- **Research Timeframe**: 1-hour (1H) bars. This removes "noise" and provides a statistically stable foundation for regime detection.
- **Validation**: Strict Time-Based Split:
  - **In-Sample (Train)**: First 70% (2024-01-01 to 2024-09-12).
  - **Out-of-Sample (Test)**: Last 30% (Unseen verification).

### 2. Core Logic (VolatilityTrendStrategy)
- **Trend Filter**: 50/200 EMA bias (relaxed to allow earlier entries).
- **Momentum Filter**: RSI (35-70 for Longs, 30-65 for Shorts) to ensure entries occur during trend continuation.
- **Volatility Scaling**: ATR-based position sizing ensures that trade size adapts to market volatility, maintaining a fixed 1% risk per trade.
- **Exits**: 
  - Dynamic Stop-Loss (1.2 * ATR)
  - Take-Profit (2.5 * ATR)
  - Time-based exit (20 bars)

---

## 📊 Backtest Performance (Stage-3 Optimized)

| Asset | Period | Sharpe Ratio | Max Drawdown | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **XAGUSD** | In-Sample | 0.92 | -1.06% | ✅ Profitable |
| **XAGUSD** | Out-of-Sample | 0.12 | -1.62% | ✅ Robust |

*Note: Model selection was performed on the training set. Final performance is reported on unseen data to ensure real-world viability.*

## 📂 Project Structure
```text
quantalytics/
├── data/
│   ├── raw/           # Raw M1 CSV files
│   └── processed/     # 1H Resampled Research Data
├── features/          # Feature engineering modules
├── strategies/        # Baseline & Regime-Adaptive strategies
├── backtests/         # Walk-forward analysis scripts
├── evaluation/        # Statistical significance tests
├── notebooks/         # EDA & visual analysis
├── strategy.py        # Primary entry point
└── README.md
```

---
**Author**: Amarendra Pratap Singh
**License**: MIT
