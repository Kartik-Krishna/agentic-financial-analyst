import yfinance as yf

def get_basic_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)

    fast_info = stock.fast_info
    info = stock.info

    market_cap = getattr(fast_info, "market_cap", None)
    current_price = getattr(fast_info, "last_price", None)

    return {
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "market_cap": market_cap,
        "current_price": current_price,
    }