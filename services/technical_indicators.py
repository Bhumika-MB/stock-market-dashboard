import pandas as pd


def add_technical_indicators(data):

    data = data.copy()

    # Daily Return (%)
    data["Daily Return"] = (
        data["Close"].pct_change() * 100
    )

    # Volatility (20-Day Rolling Standard Deviation)
    data["Volatility"] = (
        data["Daily Return"]
        .rolling(window=20)
        .std()
    )

    # RSI (14-Day)
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss

    data["RSI"] = 100 - (100 / (1 + rs))

    return data