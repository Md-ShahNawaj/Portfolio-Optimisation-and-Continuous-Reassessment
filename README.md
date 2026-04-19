# Portfolio Optimisation & Continuous Reassessment

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20Demo-FF4B4B?style=flat&logo=streamlit)](https://your-streamlit-cloud-link.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A Streamlit-based dashboard for analyzing portfolio performance, backtesting strategies, and visualizing risk metrics using S&P 500 data.

> **Note:** This project demonstrates continuous portfolio reassessment — dynamically rebalancing and optimizing holdings based on rolling performance metrics.

## Live Demo

🚀 **Try the live dashboard:** [https://your-streamlit-cloud-link.streamlit.app](https://your-streamlit-cloud-link.streamlit.app)

*(Deploy to Streamlit Cloud for free — see deployment instructions below)*

## Strategies Implemented

| Strategy | Description |
|----------|-------------|
| **Buy & Hold (SPY)** | Baseline passive strategy — buy and hold S&P 500 ETF |
| **Momentum** | Select top-performing stocks based on recent returns |
| **Mean Reversion** | Bet on prices returning to historical averages |
| **Risk Parity** | Equal risk contribution across all holdings |
| **Minimum Variance** | Optimize for lowest portfolio volatility |
| **Maximum Sharpe** | Maximize risk-adjusted returns |
| **Equal Weight** | Simple 1/N diversification across all stocks |

## Features

- **Performance Metrics**: Total return, CAGR, Sharpe ratio, max drawdown
- **Rolling Analytics**: Rolling volatility and Sharpe ratio over time
- **Monthly Heatmap**: Monthly return visualization by year
- **Strategy Comparison**: Compare multiple portfolio strategies side-by-side
- **Interactive Charts**: Plotly-powered interactive visualizations

## Tech Stack

- **Python**: pandas, numpy, matplotlib, plotly
- **Streamlit**: Web framework for the dashboard
- **Jupyter Notebook**: For data analysis and exploration

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## Project Structure

```
├── app.py                      # Main Streamlit dashboard
├── Portfolio_Optimisation.ipynb # Jupyter notebook for analysis
├── aligned_returns.csv         # Aligned daily returns for strategies
├── sp500_full_ohlcv_5y.csv     # 5-year OHLCV data for S&P 500
├── sp500_all_tickers.json      # List of S&P 500 tickers
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Data Sources

- **aligned_returns.csv**: Contains daily returns for various portfolio strategies
- **sp500_full_ohlcv_5y.csv**: Historical OHLCV data for S&P 500 stocks (5 years)
- **sp500_all_tickers.json**: Comprehensive list of S&P 500 component tickers

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **Total Return %** | Overall return from start to end date |
| **CAGR %** | Compound Annual Growth Rate |
| **Ann Return %** | Annualized return |
| **Ann Vol %** | Annualized volatility (risk) |
| **Sharpe** | Risk-adjusted return (higher is better) |
| **Max DD %** | Maximum drawdown (largest peak-to-trough decline) |

## Screenshots

| Dashboard Overview | Monthly Heatmap |
|--------------------|-----------------|
| ![Dashboard](images/dashboard.png) | ![Heatmap](images/monthly_heatmap.png) |

| Rolling Metrics | Strategy Comparison |
|-----------------|---------------------|
| ![Rolling](images/rolling_metrics.png) | ![Comparison](images/strategy_comparison.png) |

*(Add your screenshots to the `images/` folder)*

## Deployment to Streamlit Cloud

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account and select your repository
4. Set the main file path as `app.py`
5. Add your secrets (if needed) in the Streamlit Cloud settings
6. Click **Deploy**

Your live URL will be: `https://your-app-name.streamlit.app`

## License

MIT License