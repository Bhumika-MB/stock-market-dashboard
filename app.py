from services.indicators import calculate_metrics
import streamlit as st
import plotly.graph_objects as go

from services.stock_data import get_stock_data
from services.moving_averages import add_moving_averages
from services.company_info import get_company_info

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

st.write("Selected Company:", company_name)
st.write("Ticker:", ticker)

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

st.subheader("📊 Market Summary")

metrics = calculate_metrics(data)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"${metrics['current_price']:.2f}"
)

col2.metric(
    "Daily Change",
    f"{metrics['daily_change']:.2f}",
    f"{metrics['percent_change']:.2f}%"
)

col3.metric(
    "Highest Price",
    f"${metrics['highest']:.2f}"
)

col4.metric(
    "Lowest Price",
    f"${metrics['lowest']:.2f}"
)

# -------------------- Stock Chart -------------------- #
st.subheader("📈 Stock Price Chart")

if chart_type == "Line Chart":

    fig = go.Figure()

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


else:

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="Candlestick"
            )
        ]
    )

fig.update_layout(
    title=f"{selected_company} Stock Price",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    template="plotly_white",
    hovermode="x unified",
    height=650,
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig, width="stretch")
st.subheader("📊 Trading Volume")

volume_fig = go.Figure()

volume_fig.add_trace(
    go.Bar(
        x=data.index,
        y=data["Volume"],
        name="Volume"
    )
)

volume_fig.update_layout(
    title=f"{selected_company} Trading Volume",
    xaxis_title="Date",
    yaxis_title="Volume",
    template="plotly_white",
    height=300
)

st.plotly_chart(volume_fig, width="stretch")

# -------------------- Data Table -------------------- #
st.subheader("📋 Last 5 Trading Days")
st.dataframe(data.tail(), width="stretch")