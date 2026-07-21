import pandas as pd


def get_model_info():

    return pd.DataFrame({
        "Model": [
            "Linear Regression",
            "Support Vector Regression (SVR)"
        ],

        "Purpose": [
            "30-day stock price prediction",
            "Non-linear prediction comparison"
        ],

        "Status": [
            "✅ Active",
            "✅ Active"
        ]
    })