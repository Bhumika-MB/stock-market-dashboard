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

# -------------------- Page Configuration -------------------- #
st.set_page_config(
    page_title="Stock Market Prediction Dashboard",
    page_icon="📈",
    layout="wide"
)

# -------------------- Title -------------------- #
st.title("📈 Stock Market Prediction Dashboard")

st.caption("Analyze stock performance with interactive charts and real-time market data.")

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

# -------------------- Download Data -------------------- #

if ticker == "":
    st.info("👈 Select a company or enter a stock ticker.")
    st.stop()

data = get_stock_data(
    ticker,
    period_map[period]
)
data = add_moving_averages(data)
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

st.subheader("🤖 AI Stock Prediction")

if predictions is None:

    st.warning(
        "Not enough historical data to make a prediction. "
        "Try selecting a longer time period."
    )

else:

    lr_predictions = predictions["Linear Regression"]
    svr_predictions = predictions["SVR"]

    st.metric(
        "Predicted Price (30 Days)",
        f"${lr_predictions[-1]:.2f}"
    )

    prediction_dates = pd.date_range(
        start=data.index[-1],
        periods=len(lr_predictions) + 1,
        freq="B"
    )[1:]

    pred_fig = go.Figure()

    pred_fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Historical Price"
        )
    )

    pred_fig.add_trace(
        go.Scatter(
            x=prediction_dates,
            y=lr_predictions,
            mode="lines",
            name="Predicted Price",
            line=dict(dash="dash")
        )
    )

    pred_fig.update_layout(
        title="30-Day Stock Forecast",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white"
    )

    st.plotly_chart(pred_fig, width="stretch")
    st.subheader("🤖 Model Comparison")

    comparison = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Support Vector Regression"
    ],
    "Predicted Price": [
        round(lr_predictions[-1], 2),
        round(svr_predictions[-1], 2)
    ]
    })

    st.table(comparison)

    recommendation, reason = get_recommendation(
        data,
        lr_predictions[-1]
    )

    st.subheader("💡 AI Recommendation")

    st.success(recommendation)

    st.info(reason)

    st.subheader("🧠 Machine Learning Models")

    models = get_model_info()

    st.table(models)