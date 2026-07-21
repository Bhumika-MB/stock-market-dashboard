def get_recommendation(data, predicted_price):

    current_price = data["Close"].iloc[-1]
    sma20 = data["SMA20"].iloc[-1]
    rsi = data["RSI"].iloc[-1]

    if predicted_price > current_price and current_price > sma20:

        if rsi > 70:
            return (
                "🟢 BUY",
                "The model predicts an upward trend and the stock is trading above its 20-Day SMA. However, the RSI indicates the stock is currently overbought."
            )

        return (
            "🟢 BUY",
            "The model predicts an upward trend and the stock is trading above its 20-Day SMA."
        )

    elif predicted_price < current_price and current_price < sma20:

        if rsi < 30:
            return (
                "🔴 SELL",
                "The model predicts a downward trend and the stock is trading below its 20-Day SMA. RSI also indicates bearish momentum."
            )

        return (
            "🔴 SELL",
            "The model predicts a downward trend and the stock is trading below its 20-Day SMA."
        )

    else:
        return (
            "🟡 HOLD",
            "Prediction and technical indicators are mixed. Waiting for a stronger market signal is recommended."
        )