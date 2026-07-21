import pandas as pd

from services.indicators import calculate_metrics
import streamlit as st
import plotly.graph_objects as go

from services.stock_data import get_stock_data
from services.moving_averages import add_moving_averages
from services.company_info import get_company_info
from models.predictor import predict_stock_price
from services.recommendation import get_recommendation
from services.model_info import get_model_info
from services.technical_indicators import add_technical_indicators
from services.risk_analysis import classify_risk
from services.trend import get_market_trend

# -------------------- Page Configuration -------------------- #
st.set_page_config(
    page_title="Stock Market Prediction Dashboard",
    page_icon="📈",
    layout="wide"
)

# -------------------- Title -------------------- #
st.title("📈 Stock Market Prediction Dashboard")

st.caption(
    "Analyze stock performance using technical indicators, machine learning models, and interactive visualizations."
)

st.divider()

# -------------------- Sidebar -------------------- #
popular_companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Meta": "META",
    "Netflix": "NFLX",
    "AMD": "AMD",
    "Intel": "INTC",
    "Reliance": "RELIANCE.NS",
    "Infosys": "INFY.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Other...": ""
}

selected_company = st.sidebar.selectbox(
    "⭐ Popular Companies",
    list(popular_companies.keys())
)
if selected_company == "Other...":

    ticker = st.sidebar.text_input(
        "🔍 Enter Stock Ticker",
        placeholder="Example: AAPL or RELIANCE.NS"
    ).upper()

    company_name = ticker

else:

    ticker = popular_companies[selected_company]
    company_name = selected_company


st.sidebar.markdown("---")

period = st.sidebar.selectbox(
    "📅 Select Time Period",
    {
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "2 Years": "2y",
        "5 Years": "5y"
    }
)

period_map = {
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y"
}

st.sidebar.markdown("---")

chart_type = st.sidebar.radio(
    "📊 Chart Type",
    ["Line Chart", "Candlestick"]
)
st.sidebar.markdown("---")

show_sma20 = st.sidebar.checkbox(
    "Show 20-Day SMA",
    value=True
)

show_sma50 = st.sidebar.checkbox(
    "Show 50-Day SMA",
    value=True
)

show_ema20 = st.sidebar.checkbox(
    "Show 20-Day EMA",
    value=True
)

# -------------------- Download Data -------------------- #

if ticker == "":
    st.info("👈 Select a company or enter a stock ticker.")
    st.stop()

data = get_stock_data(
    ticker,
    period_map[period]
)
data = add_moving_averages(data)
data = add_technical_indicators(data)
company = get_company_info(ticker)

if len(data) < 30:
    predictions = None
else:
    predictions = predict_stock_price(data)


st.info(f"### 📌 Currently Viewing: {selected_company} ({ticker})")
st.subheader("🏢 Company Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Company:**", company["name"])
    st.write("**Sector:**", company["sector"])
    st.write("**Industry:**", company["industry"])

with col2:
    st.write("**Country:**", company["country"])
    st.write("**Website:**", company["website"])

    market_cap = company["market_cap"]

    if market_cap:
        st.write(f"**Market Cap:** ${market_cap:,.0f}")
    else:
        st.write("**Market Cap:** N/A")

# -------------------- KPI Cards -------------------- #

# -------------------- Historical Stock Chart -------------------- #

st.subheader("📈 Historical Stock Chart")

fig = go.Figure()

if chart_type == "Line Chart":

    # Closing Price
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Closing Price",
            line=dict(width=3)
        )
    )

    # 20-Day SMA
    if show_sma20:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["SMA20"],
                mode="lines",
                name="20-Day SMA"
            )
        )

    # 50-Day SMA
    if show_sma50:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["SMA50"],
                mode="lines",
                name="50-Day SMA"
            )
        )

    # 20-Day EMA
    if show_ema20:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["EMA20"],
                mode="lines",
                name="20-Day EMA"
            )
        )

else:

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Candlestick"
        )
    )

fig.update_layout(
    title=f"{selected_company} Historical Stock Price",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_white",
    hovermode="x unified",
    height=600,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, width="stretch")
# -------------------- Download Stock Data -------------------- #

csv = data.to_csv().encode("utf-8")

st.download_button(
    label="⬇ Download Stock Data (CSV)",
    data=csv,
    file_name=f"{ticker}_stock_data.csv",
    mime="text/csv"
)

st.subheader("📊 Technical Indicators")

col1, col2, col3 = st.columns(3)

# -------- Daily Return -------- #

with col1:

    st.metric(
        "Daily Return",
        f"{data['Daily Return'].iloc[-1]:.2f}%"
    )


# -------- Volatility -------- #

with col2:

    volatility = data["Volatility"].iloc[-1]

    if pd.isna(volatility):

        st.metric(
            "Volatility",
            "--"
        )

        st.caption("Need 20 trading days")

    else:

        st.metric(
            "Volatility",
            f"{volatility:.2f}"
        )


# -------- RSI -------- #

with col3:

    rsi = data["RSI"].iloc[-1]

    st.metric(
        "RSI",
        f"{rsi:.2f}"
    )

    if rsi > 70:
        st.caption("Overbought")

    elif rsi < 30:
        st.caption("Oversold")

    else:
        st.caption("Neutral")

st.subheader("📈 Market Trend")

trend, trend_reason = get_market_trend(data)

if "Bullish" in trend:
    st.success(trend)

elif "Bearish" in trend:
    st.error(trend)

else:
    st.warning(trend)

st.caption(trend_reason)

st.subheader("💡 AI Recommendation")

st.success(recommendation)
st.info(reason)

st.subheader("🛡 Risk Analysis")

risk = classify_risk(data)

if "Low" in risk:
        st.success(risk)

elif "Medium" in risk:
        st.warning(risk)

else:
        st.error(risk)

st.subheader("🧠 Machine Learning Models")

models = get_model_info()

st.table(models)
st.caption(
    "The dashboard compares predictions from Linear Regression and Support Vector Regression (SVR) and automatically displays the prediction from the model with the higher R² score."
)