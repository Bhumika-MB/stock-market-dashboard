import pandas as pd


def get_model_info():

    return pd.DataFrame({
        "Model": [
            "Linear Regression",
            "Support Vector Regression (SVR)",
            "LSTM",
            "PCA + Linear Regression"
        ],

        "Purpose": [
            "Current prediction model",
            "Non-linear regression comparison",
            "Deep learning time-series forecasting",
            "Dimensionality reduction"
        ],

        "Status": [
            "✅ Active",
            "✅ Active",
            "🚧 Future Enhancement",
            "🚧 Future Enhancement"
        ]
    })