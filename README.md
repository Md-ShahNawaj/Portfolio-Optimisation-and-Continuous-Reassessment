# Portfolio Optimisation & Continuous Reassessment

A Streamlit-based dashboard for analyzing portfolio performance, backtesting strategies, and visualizing risk metrics using S&P 500 data.

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

## License

MIT License