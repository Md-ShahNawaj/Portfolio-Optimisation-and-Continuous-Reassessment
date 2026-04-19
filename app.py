import re
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Portfolio Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# CSS (keep your style)
# -----------------------------
st.markdown(
    """
<style>
.block-container { padding-top: 0.5rem; padding-bottom: 0.6rem; }

.sticky-title-container {
    position: sticky; top: 0; z-index: 999;
    background: rgba(10, 12, 16, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 12px 10px 10px 10px;
    margin-bottom: 10px;
}
.sticky-title {
    font-size: 40px; font-weight: 850; margin: 0;
    line-height: 1.1; letter-spacing: 0.2px;
}
div[data-testid="stTabs"] button {
  font-size: 14px !important;
  padding: 8px 12px !important;
  border-radius: 12px !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
  border-bottom: 3px solid rgba(255,255,255,0.55) !important;
}
div[data-testid="stTabs"] { margin-top: 6px; }
div[data-testid="stTabs"] > div { gap: 8px; }
section[data-testid="stSidebar"] .stExpander { border-radius: 14px; }
section[data-testid="stSidebar"] button { border-radius: 10px; }
div[data-testid="stMetric"] {
  padding: 8px 10px 6px 10px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.07);
}
.js-plotly-plot, .plot-container { margin-top: -6px; }
header[data-testid="stHeader"] { background: transparent; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="sticky-title-container">
  <div class="sticky-title">Portfolio Dashboard</div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Constants & helpers
# -----------------------------
TRADING_DAYS = 252


def safe_read_csv(path) -> pd.DataFrame:
    df0 = pd.read_csv(path)

    # Parse date index
    if "Date" in df0.columns:
        df0["Date"] = pd.to_datetime(df0["Date"], errors="coerce")
        df0 = df0.set_index("Date")
    else:
        df0.iloc[:, 0] = pd.to_datetime(df0.iloc[:, 0], errors="coerce")
        df0 = df0.set_index(df0.columns[0])

    df0.index = pd.to_datetime(df0.index, errors="coerce")
    df0 = df0[~df0.index.isna()]
    df0 = df0.sort_index()

    # Convert numeric
    df0 = df0.apply(pd.to_numeric, errors="coerce").dropna(how="all")
    return df0


def parse_strategy_name(col: str):
    # 'SPY Buy & Hold'
    if col.strip().startswith("SPY"):
        return ("SPY", "Buy&Hold")

    m = re.match(r"^(.*?)\s*\((.*?)\)\s*$", col.strip())
    if m:
        return (m.group(1).strip(), m.group(2).strip())
    return (col.strip(), "Unknown")


def growth_from_returns(r: pd.DataFrame) -> pd.DataFrame:
    return (1.0 + r).cumprod()


def drawdown_from_growth(g: pd.Series) -> pd.Series:
    peak = g.cummax()
    return g / peak - 1.0


def cagr_from_growth(g: pd.Series) -> float:
    g = g.dropna()
    if len(g) < 2:
        return np.nan
    years = len(g) / TRADING_DAYS
    return float(g.iloc[-1] ** (1 / years) - 1) if years > 0 else np.nan


def perf_metrics(returns: pd.Series, rf_annual: float) -> dict:
    r = returns.dropna()
    if len(r) < 20:
        return {}

    g = (1 + r).cumprod()
    cagr = cagr_from_growth(g)

    ann_vol = float(r.std() * np.sqrt(TRADING_DAYS))
    ann_ret = float(r.mean() * TRADING_DAYS)
    sharpe = (ann_ret - rf_annual) / ann_vol if ann_vol > 0 else np.nan



    # Max drawdown + Calmar
    dd = drawdown_from_growth(g)
    mdd = float(dd.min())


    total_return = float(g.iloc[-1] - 1.0)

    return {
        "Total Return %": total_return * 100,
        "CAGR %": cagr * 100,
        "Ann Return %": ann_ret * 100,
        "Ann Vol %": ann_vol * 100,
        "Sharpe": sharpe,
        "Max DD %": mdd * 100,
    }


def rolling_ann_vol(returns: pd.Series, window=63) -> pd.Series:
    return returns.rolling(window).std() * np.sqrt(TRADING_DAYS)


def rolling_sharpe(returns: pd.Series, rf_annual: float, window=126) -> pd.Series:
    rf_daily = rf_annual / TRADING_DAYS
    excess = returns - rf_daily
    roll_ret = excess.rolling(window).mean() * TRADING_DAYS
    roll_vol = returns.rolling(window).std() * np.sqrt(TRADING_DAYS)
    return roll_ret / roll_vol


def monthly_heatmap(returns: pd.Series) -> pd.DataFrame:
    r = returns.dropna()
    if r.empty:
        return pd.DataFrame()

    m = (1 + r).resample("ME").prod() - 1
    hm = pd.DataFrame({"ret": m})
    hm["Year"] = hm.index.year
    hm["Month"] = hm.index.month

    pivot = hm.pivot(index="Year", columns="Month", values="ret").sort_index()
    pivot = pivot.reindex(columns=range(1, 13))
    pivot.columns = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return pivot * 100


# -----------------------------
# Load dataset
# -----------------------------
DEFAULT_PATH = "aligned_returns.csv"
try:
    df_all = safe_read_csv(DEFAULT_PATH)
except Exception as e:
    st.error(f"Failed to load dataset: {DEFAULT_PATH}")
    st.code(str(e))
    st.stop()

if df_all.empty:
    st.error("CSV loaded but empty. Check aligned_returns.csv.")
    st.stop()

# -----------------------------
# Build metadata
# -----------------------------
meta = pd.DataFrame({"col": df_all.columns})
meta[["Model", "Freq"]] = meta["col"].apply(lambda x: pd.Series(parse_strategy_name(x)))

models_available = sorted(meta["Model"].unique().tolist())
freq_order = ["W", "M", "Y", "Buy&Hold"]
freqs_available = [f for f in freq_order if f in meta["Freq"].unique().tolist()]
if not freqs_available:
    freqs_available = sorted(meta["Freq"].unique().tolist())

# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar.expander("1) Portfolio Models", expanded=True):
    default_models = [m for m in ["EW", "MinVar", "BL"] if m in models_available]
    if "SPY" in models_available:
        default_models += ["SPY"]

    selected_models = st.multiselect(
        "Select model(s)",
        options=models_available,
        default=default_models if default_models else models_available[: min(4, len(models_available))],
    )

with st.sidebar.expander("2) Rebalance Frequency", expanded=True):
    default_freq = "M" if "M" in freqs_available else freqs_available[0]
    selected_freq = st.radio("Frequency", options=freqs_available, index=freqs_available.index(default_freq))

with st.sidebar.expander("3) Date Range", expanded=True):
    min_date = df_all.index.min().date()
    max_date = df_all.index.max().date()
    start_date, end_date = st.date_input(
        "Select period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

with st.sidebar.expander("4) Risk settings", expanded=False):
    rf = st.number_input("Risk-free rate (annual)", value=0.03, min_value=0.0, max_value=0.2, step=0.005)

with st.sidebar.expander("5) Display", expanded=False):
    include_spy = st.checkbox("Always include SPY benchmark", value=True)
    legend_model_only = st.checkbox("Legend shows model names only", value=True)
    rolling_vol_window = st.slider("Rolling Vol window (days)", 21, 252, 63, step=21)
    rolling_sharpe_window = st.slider("Rolling Sharpe window (days)", 63, 252, 126, step=21)

# -----------------------------
# Filter columns (model + frequency)
# -----------------------------
filtered_cols = meta[(meta["Model"].isin(selected_models)) & (meta["Freq"] == selected_freq)]["col"].tolist()

if include_spy:
    spy_cols = meta[meta["Model"] == "SPY"]["col"].tolist()
    for c in spy_cols:
        if c not in filtered_cols:
            filtered_cols.append(c)

if not filtered_cols:
    st.warning("No strategies match your selection (models + frequency).")
    st.stop()

df = df_all[filtered_cols].copy()

# Date range filter
df = df.loc[(df.index.date >= start_date) & (df.index.date <= end_date)]
df = df.dropna(how="all")
if df.empty:
    st.warning("No data in the selected date range.")
    st.stop()

# Rename columns for legend if requested
if legend_model_only:
    rename_map = {c: parse_strategy_name(c)[0] for c in df.columns}
    df = df.rename(columns=rename_map)

# -----------------------------
# Compute metrics & series
# -----------------------------
growth = growth_from_returns(df)

metrics_rows = []
for col in df.columns:
    m = perf_metrics(df[col], rf)
    if m:
        metrics_rows.append([col, *m.values()])

metrics = pd.DataFrame(
    metrics_rows,
    columns=["Strategy"] + list(perf_metrics(df.iloc[:, 0].dropna(), rf).keys()),
).set_index("Strategy")

# Identify benchmark
spy_name = "SPY" if "SPY" in df.columns else None

# Focus strategy for deep dive (investor-friendly)
with st.sidebar.expander("6) Focus Strategy (Deep Dive)", expanded=False):
    focus_default = "MinVar" if "MinVar" in df.columns else df.columns[0]
    focus_strategy = st.selectbox("Focus strategy", options=list(df.columns), index=list(df.columns).index(focus_default))

# -----------------------------
# Tabs
# -----------------------------
tab_overview, tab_risk, tab_deepdive, tab_data = st.tabs(
    ["Overview", "Risk & Drawdowns", "Deep Dive", "Data"]
)

# -----------------------------
# Overview tab
# -----------------------------
with tab_overview:
    st.markdown("### Key Investor Summary")

    if not metrics.empty:
        best_sharpe = metrics["Sharpe"].idxmax()
        best_cagr = metrics["CAGR %"].idxmax()
        lowest_vol = metrics["Ann Vol %"].idxmin()

        c1, c2, c3 = st.columns(3)
        c1.metric("Best Sharpe", best_sharpe, f"{metrics.loc[best_sharpe,'Sharpe']:.2f}")
        c2.metric("Best CAGR", best_cagr, f"{metrics.loc[best_cagr,'CAGR %']:.2f}%")
        c3.metric("Lowest Volatility", lowest_vol, f"{metrics.loc[lowest_vol,'Ann Vol %']:.2f}%")

    fig_growth = px.line(
        growth,
        x=growth.index,
        y=growth.columns,
        labels={"value": "Growth"},
        title=f"Cumulative Growth (£1) — Frequency: {selected_freq}",
    )
    fig_growth.update_layout(height=360, margin=dict(l=18, r=18, t=60, b=18), legend_title_text="")
    st.plotly_chart(fig_growth, use_container_width=True)

    st.markdown("### Summary Table")
    st.dataframe(metrics.sort_values("Sharpe", ascending=False), use_container_width=True, height=300)

    st.markdown("### Risk–Return Snapshot")
    if not metrics.empty:
        scatter_df = metrics.reset_index().rename(columns={"index": "Strategy"})
        fig_scatter = px.scatter(
            scatter_df,
            x="Ann Vol %",
            y="CAGR %",
            hover_name="Strategy",
            size=np.clip(scatter_df["Sharpe"].fillna(0).abs(), 0.1, None),
            title="Risk–Return Scatter (bubble size ~ |Sharpe|)",
        )
        fig_scatter.update_layout(height=320, margin=dict(l=18, r=18, t=50, b=18))
        st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Risk & Drawdowns tab
# -----------------------------
with tab_risk:
    st.markdown("### Drawdowns (Underwater Plot)")
    dd_df = pd.DataFrame({c: drawdown_from_growth(growth[c]) for c in growth.columns})
    fig_dd = px.line(dd_df, x=dd_df.index, y=dd_df.columns, labels={"value": "Drawdown"}, title="Drawdowns Over Time")
    fig_dd.update_layout(height=360, margin=dict(l=18, r=18, t=60, b=18), legend_title_text="")
    st.plotly_chart(fig_dd, use_container_width=True)

    st.markdown("### Rolling Risk Metrics")
    colA, colB = st.columns(2)

    with colA:
        rv = pd.DataFrame({c: rolling_ann_vol(df[c], window=rolling_vol_window) for c in df.columns})
        fig_rv = px.line(
            rv,
            x=rv.index,
            y=rv.columns,
            labels={"value": "Ann Vol"},
            title=f"Rolling Annualised Volatility ({rolling_vol_window}D)",
        )
        fig_rv.update_layout(height=320, margin=dict(l=18, r=18, t=60, b=18), legend_title_text="")
        st.plotly_chart(fig_rv, use_container_width=True)

    with colB:
        rs = pd.DataFrame({c: rolling_sharpe(df[c], rf, window=rolling_sharpe_window) for c in df.columns})
        fig_rs = px.line(
            rs,
            x=rs.index,
            y=rs.columns,
            labels={"value": "Sharpe"},
            title=f"Rolling Sharpe ({rolling_sharpe_window}D)",
        )
        fig_rs.update_layout(height=320, margin=dict(l=18, r=18, t=60, b=18), legend_title_text="")
        st.plotly_chart(fig_rs, use_container_width=True)

# -----------------------------
# Deep Dive tab
# -----------------------------
with tab_deepdive:
    st.markdown(f"### Focus Strategy: **{focus_strategy}**")

    r = df[focus_strategy].dropna()
    g = growth[focus_strategy].dropna()
    dd = drawdown_from_growth(g).dropna()

    m = perf_metrics(r, rf)
    if m:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("CAGR", f"{m['CAGR %']:.2f}%")
        k2.metric("Volatility", f"{m['Ann Vol %']:.2f}%")
        k3.metric("Sharpe", f"{m['Sharpe']:.2f}")
        k4.metric("Max Drawdown", f"{m['Max DD %']:.2f}%")

        k5, k6, k7, k8 = st.columns(4)
        k7.metric("Total Return", f"{m['Total Return %']:.2f}%")
        k8.metric("Ann Return", f"{m['Ann Return %']:.2f}%")

    st.markdown("#### Return Distribution (Daily)")
    fig_hist = px.histogram(r, nbins=70, title="")
    fig_hist.update_layout(height=320, margin=dict(l=18, r=18, t=60, b=18))
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("#### Monthly Returns Heatmap (%)")
    hm = monthly_heatmap(r)
    if hm.empty:
        st.info("Not enough data for monthly heatmap.")
    else:
        fig_hm = px.imshow(
            hm,
            aspect="auto",
            title="",
        )
        fig_hm.update_layout(height=420, margin=dict(l=18, r=18, t=60, b=18))
        st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown("")
    if spy_name and spy_name in df.columns and focus_strategy != spy_name:
        compare = pd.DataFrame({
            focus_strategy: growth[focus_strategy],
            "SPY": growth[spy_name]
        }).dropna()

        fig_cmp = px.line(compare, x=compare.index, y=compare.columns, title="Growth Comparison: Focus vs SPY")
        fig_cmp.update_layout(height=320, margin=dict(l=18, r=18, t=60, b=18), legend_title_text="")
        st.plotly_chart(fig_cmp, use_container_width=True)
    else:
        st.caption("Benchmark not available in current selection (or focus is SPY).")

# -----------------------------
# Data tab
# -----------------------------
with tab_data:
    st.markdown("### Data Preview (Daily Returns)")
    st.dataframe(df.head(30), use_container_width=True, height=300)

    st.download_button(
        "Download filtered daily returns (CSV)",
        df.to_csv().encode("utf-8"),
        file_name=f"filtered_returns_{selected_freq}_{start_date}_{end_date}.csv",
        mime="text/csv",
    )
