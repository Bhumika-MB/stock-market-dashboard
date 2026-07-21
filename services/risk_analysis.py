import pandas as pd


def classify_risk(data):

    daily_returns = data["Close"].pct_change()

    volatility = daily_returns.std()

    if volatility < 0.015:
        return "🟢 Low Risk"

    elif volatility < 0.03:
        return "🟡 Medium Risk"

    else:
        return "🔴 High Risk"
    