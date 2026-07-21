def get_market_trend(data):

    latest_close = data["Close"].iloc[-1]
    latest_sma20 = data["SMA20"].iloc[-1]

    if latest_close > latest_sma20:
        return "🟢 Bullish", "Price is trading above the 20-Day SMA."

    elif latest_close < latest_sma20:
        return "🔴 Bearish", "Price is trading below the 20-Day SMA."

    else:
        return "🟡 Neutral", "Price is close to the 20-Day SMA."