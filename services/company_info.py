import yfinance as yf

def get_company_info(ticker):

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "name": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "country": info.get("country", "N/A"),
        "website": info.get("website", "N/A"),
        "market_cap": info.get("marketCap", 0)
    }