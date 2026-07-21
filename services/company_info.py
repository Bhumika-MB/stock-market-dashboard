import yfinance as yf


def get_company_info(ticker):

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "name": info.get("longName", ticker),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "country": info.get("country", "N/A"),
            "website": info.get("website", "N/A"),
            "market_cap": info.get("marketCap")
        }

    except Exception:

        return {
            "name": ticker,
            "sector": "N/A",
            "industry": "N/A",
            "country": "N/A",
            "website": "N/A",
            "market_cap": None
        }