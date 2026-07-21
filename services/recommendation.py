def get_recommendation(data, predicted_price):

    current_price = data["Close"].iloc[-1]

    sma20 = data["SMA20"].iloc[-1]

    if predicted_price > current_price and current_price > sma20:
        return (
            "🟢 BUY",
            "Model predicts an upward trend and the stock is trading above its 20-Day SMA."
        )

    elif predicted_price < current_price and current_price < sma20:
        return (
            "🔴 SELL",
            "Model predicts a downward trend and the stock is trading below its 20-Day SMA."
        )

    else:
        return (
            "🟡 HOLD",
            "Current trend is neutral. Wait for a clearer signal."
        )