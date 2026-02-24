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

def get_financial_statements(ticker:str):
    stock = yf.Ticker(ticker)

    income_stmt = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow

    return income_stmt, balance_sheet, cash_flow