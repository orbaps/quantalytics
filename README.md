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

### 3. Exploratory Analysis
Run the notebooks to validate regime detection logic.
```bash
# Check notebooks/exploration.ipynb for regime visualization
```

---

## 🏗️ Strategy Benchmarking (Control Group)
### 1. Baseline Momentum Strategy
An intentionally simple control group to evaluate benchmark performance:
- **Rule**: Long if Rolling Momentum > 0; Flat otherwise.
- **Sizing**: Fixed position size (1 unit).
- **Complexity**: Baseline logic, no regime awareness, no leverage.

---

## 🛠️ Data Methodology
- **Raw Data**: 1-minute (M1) institutional feeds.
- **Research Timeframe**: 1-hour (1H) bars. This removes "noise" and provides a statistically stable foundation for regime detection.
- **Validation**: Strict Time-Based Split:
  - **In-Sample (Train)**: First 70% (2024-01-01 to 2024-09-12).
  - **Out-of-Sample (Test)**: Last 30% (Unseen verification).

---

## 📂 Project Structure
```text
quantalytics/
├── data/
│   ├── raw/           # Raw M1 CSV files
│   └── processed/     # 1H Resampled Research Data
├── features/          # Feature engineering modules (Volatility, Regimes)
├── strategies/        # Baseline & Regime-Adaptive strategies
├── backtests/         # Walk-forward analysis scripts
├── evaluation/        # Statistical significance tests
├── notebooks/         # EDA & visual analysis
├── strategy.py        # Placeholder (Development Phase)
└── README.md
```

---
**Author**: Amarendra Pratap Singh
**License**: MIT
