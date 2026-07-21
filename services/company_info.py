import yfinance as yf

# Fallback details for popular companies
FALLBACK_COMPANIES = {
    "AAPL": {
        "name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "country": "United States",
        "website": "https://www.apple.com"
    },
    "MSFT": {
        "name": "Microsoft Corporation",
        "sector": "Technology",
        "industry": "Software",
        "country": "United States",
        "website": "https://www.microsoft.com"
    },
    "NVDA": {
        "name": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "country": "United States",
        "website": "https://www.nvidia.com"
    },
    "TSLA": {
        "name": "Tesla Inc.",
        "sector": "Automotive",
        "industry": "Electric Vehicles",
        "country": "United States",
        "website": "https://www.tesla.com"
    },
    "AMZN": {
        "name": "Amazon.com Inc.",
        "sector": "Consumer Cyclical",
        "industry": "Internet Retail",
        "country": "United States",
        "website": "https://www.amazon.com"
    },
    "GOOGL": {
        "name": "Alphabet Inc.",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "country": "United States",
        "website": "https://abc.xyz"
    },
    "META": {
        "name": "Meta Platforms Inc.",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "country": "United States",
        "website": "https://about.meta.com"
    },
    "NFLX": {
        "name": "Netflix Inc.",
        "sector": "Communication Services",
        "industry": "Entertainment",
        "country": "United States",
        "website": "https://www.netflix.com"
    },
    "AMD": {
        "name": "Advanced Micro Devices",
        "sector": "Technology",
        "industry": "Semiconductors",
        "country": "United States",
        "website": "https://www.amd.com"
    },
    "INTC": {
        "name": "Intel Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "country": "United States",
        "website": "https://www.intel.com"
    },
    "RELIANCE.NS": {
        "name": "Reliance Industries Ltd.",
        "sector": "Energy",
        "industry": "Oil & Gas",
        "country": "India",
        "website": "https://www.ril.com"
    },
    "INFY.NS": {
        "name": "Infosys Ltd.",
        "sector": "Technology",
        "industry": "IT Services",
        "country": "India",
        "website": "https://www.infosys.com"
    },
    "TCS.NS": {
        "name": "Tata Consultancy Services",
        "sector": "Technology",
        "industry": "IT Services",
        "country": "India",
        "website": "https://www.tcs.com"
    },
    "HDFCBANK.NS": {
        "name": "HDFC Bank",
        "sector": "Financial Services",
        "industry": "Banks",
        "country": "India",
        "website": "https://www.hdfcbank.com"
    },
    "ICICIBANK.NS": {
        "name": "ICICI Bank",
        "sector": "Financial Services",
        "industry": "Banks",
        "country": "India",
        "website": "https://www.icicibank.com"
    },
    "SBIN.NS": {
        "name": "State Bank of India",
        "sector": "Financial Services",
        "industry": "Banks",
        "country": "India",
        "website": "https://sbi.co.in"
    }
}


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
            "market_cap": info.get("marketCap", None)
        }

    except Exception:

        fallback = FALLBACK_COMPANIES.get(ticker)

        if fallback:
            return {
                "name": fallback["name"],
                "sector": fallback["sector"],
                "industry": fallback["industry"],
                "country": fallback["country"],
                "website": fallback["website"],
                "market_cap": None
            }

        return {
            "name": ticker,
            "sector": "N/A",
            "industry": "N/A",
            "country": "N/A",
            "website": "N/A",
            "market_cap": None
        }