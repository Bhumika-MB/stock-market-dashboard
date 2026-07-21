import pandas as pd


def add_moving_averages(data):

    data = data.copy()

    # Simple Moving Averages
    data["SMA20"] = data["Close"].rolling(window=20).mean()

    data["SMA50"] = data["Close"].rolling(window=50).mean()

    # Exponential Moving Average
    data["EMA20"] = data["Close"].ewm(
        span=20,
        adjust=False
    ).mean()

    return data