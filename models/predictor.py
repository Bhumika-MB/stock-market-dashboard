import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import r2_score


def predict_stock_price(data):

    df = data.copy()

    df = df[["Close"]].dropna()

    if len(df) < 30:
        return None

    X = np.arange(len(df)).reshape(-1, 1)
    y = df["Close"].values

    # ---------------- Linear Regression ---------------- #

    lr = LinearRegression()
    lr.fit(X, y)

    lr_train_prediction = lr.predict(X)
    lr_score = r2_score(y, lr_train_prediction)

    future_days = 30

    future_X = np.arange(
        len(df),
        len(df) + future_days
    ).reshape(-1, 1)

    lr_prediction = lr.predict(future_X)

    # ---------------- SVR ---------------- #

    svr = SVR(kernel="rbf")

    svr.fit(X, y)

    svr_train_prediction = svr.predict(X)
    svr_score = r2_score(y, svr_train_prediction)

    svr_prediction = svr.predict(future_X)
    
    print("Returning:", {
    "Linear Regression": lr_prediction,
    "SVR": svr_prediction,
    "LR Score": lr_score,
    "SVR Score": svr_score
})

    return {
    "Linear Regression": lr_prediction,
    "SVR": svr_prediction,
    "LR Score": lr_score,
    "SVR Score": svr_score
}