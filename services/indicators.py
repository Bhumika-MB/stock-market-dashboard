def calculate_metrics(data):
    """
    Returns stock summary metrics.
    """

    latest = data.iloc[-1]
    previous = data.iloc[-2]

    change = latest["Close"] - previous["Close"]
    percent_change = (change / previous["Close"]) * 100

    return {
        "current_price": latest["Close"],
        "daily_change": change,
        "percent_change": percent_change,
        "highest": data["High"].max(),
        "lowest": data["Low"].min(),
    }