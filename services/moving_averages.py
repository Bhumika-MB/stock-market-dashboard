import pandas as pd


def add_moving_averages(data):
    """
    Add Simple Moving Averages to stock data.
    """

    data = data.copy()

    data["SMA20"] = data["Close"].rolling(window=20).mean()
    data["SMA50"] = data["Close"].rolling(window=50).mean()

    return data