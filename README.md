# 📊 Portfolio Optimisation & Continuous Reassessment

A **quantitative finance and data analytics project** that develops a complete **portfolio research pipeline**, combining portfolio optimisation, backtesting, and interactive visualisation using **S&P 500 equity data**.

---

## 🌐 Live Demo

Explore the interactive dashboard here:  
👉 https://portfolio-optimisation-dashboard.streamlit.app/

---

## 🚀 Project Overview

This project implements an **end-to-end portfolio optimisation framework**, covering:

- Data collection and preprocessing  
- Risk and return estimation  
- Portfolio construction using multiple strategies  
- Backtesting under realistic conditions  
- Performance evaluation using financial metrics  
- Interactive dashboard for result interpretation  

The study focuses on understanding how **portfolio strategies and rebalancing frequency impact risk-adjusted performance**.

---

## 🎯 Research Objectives

- Construct a **clean and aligned dataset** of S&P 500 stocks (~496 assets)  
- Compare portfolio strategies:
  - Equal Weight (EW)  
  - Minimum Variance (MinVar)  
  - Black-Litterman (BL)  
- Analyse the impact of **rebalancing frequency**:
  - Weekly  
  - Monthly  
  - Yearly  
  - Buy & Hold  
- Perform **realistic backtesting (no look-ahead bias)**  
- Develop an **interactive Streamlit dashboard**  

---

## 📊 Key Findings

- **Minimum Variance (Monthly Rebalancing)** performed best:
  - CAGR: ~20.52%  
  - Sharpe Ratio: 1.44  
  - Max Drawdown: ~-11.99%  

- **Rebalancing improves risk control**
  - Lower drawdowns compared to Buy & Hold  

- **Monthly rebalancing is optimal**
  - Best balance between responsiveness and stability  

- **Black-Litterman performs strongly**
  - Good risk-adjusted returns but sensitive to assumptions  

---

## 🧠 Methodology

### 📌 Data

- S&P 500 equity dataset (~496 stocks)  
- Period: January 2021 – January 2026  
- Benchmark: SPY ETF  

---

### 📌 Data Preprocessing

- Missing value handling (forward/backward fill)  
- Time alignment across all assets  
- Daily return calculation  
- Exploratory Data Analysis:
  - Correlation analysis  
  - Normalisation (Z-score, Min-Max)  
  - Trend and smoothing analysis  

---

### 📌 Risk Estimation

- **Ledoit-Wolf shrinkage covariance estimator**  
- Reduces noise and improves stability in high-dimensional portfolios  

---

### 📌 Expected Return Model

- **Capital Asset Pricing Model (CAPM)**  
- Used as structured input for portfolio construction  
- Not treated as a direct return forecast  

---

### 📌 Portfolio Strategies

#### Equal Weight (EW)
- Equal allocation across all assets  
- Simple and robust baseline  

#### Minimum Variance (MinVar)
- Minimises portfolio volatility  
- Uses covariance matrix for optimisation  

#### Black-Litterman (BL)
- Bayesian framework  
- Combines market equilibrium with investor/model views  
- Produces more stable portfolio weights  

---

### 📌 Backtesting Framework

- Daily portfolio evaluation  
- Expanding window estimation  
- No look-ahead bias  
- Fixed asset universe  

Portfolio value is calculated as:
V_t = V_{t-1} (1 + r_{p,t})

---

### 📌 Rebalancing Strategies

- Weekly  
- Monthly  
- Yearly  
- Buy & Hold  

---

### 📌 Performance Metrics

- Compound Annual Growth Rate (CAGR)  
- Annualised Volatility  
- Sharpe Ratio  
- Maximum Drawdown  

---

## 📊 Dashboard Features

The Streamlit dashboard provides:

- 📈 Cumulative return visualisation  
- 📉 Drawdown analysis  
- 📊 Risk-return scatter plots  
- 📅 Rolling performance metrics  
- 📦 Portfolio allocation insights  
- ⚙️ Strategy comparison tools  

---

## 🛠️ Tech Stack

- **Python**: pandas, numpy, matplotlib, plotly  
- **Streamlit**: Interactive dashboard  
- **Jupyter Notebook**: Data analysis  
- **Finance Models**:
  - CAPM  
  - Minimum Variance  
  - Black-Litterman  
- **Statistics**:
  - Ledoit-Wolf covariance shrinkage  

---

## ⚙️ Installation

Install dependencies:
```
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
├── app.py
├── Portfolio_Optimisation.ipynb
├── aligned_returns.csv
├── sp500_full_ohlcv_5y.csv
├── sp500_all_tickers.json
├── requirements.txt
└── README.md
```

---

## ⚠️ Limitations

- Transaction costs and slippage are not included  
- No out-of-sample validation  
- Potential survivorship bias  
- Simplified portfolio constraints  

---

## 🔮 Future Improvements

- Include transaction costs and turnover constraints  
- Apply machine learning for return prediction  
- Perform walk-forward validation  
- Enhance Black-Litterman with predictive signals  

---

## 🎯 Why This Project Matters

This project demonstrates:

- End-to-end data science workflow  
- Quantitative finance expertise  
- Real-world backtesting methodology  
- Risk analysis and portfolio optimisation  
- Deployment of interactive dashboards  

---

## 📜 License

MIT License