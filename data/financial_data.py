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

def compute_ratios(income_stmt, balance_sheet):
    latest_year = income_stmt.columns[0]
    previous_year = income_stmt.columns[1]

    #Core metrics
    total_revenue = income_stmt.loc["Total Revenue", latest_year]
    net_income = income_stmt.loc["Net Income", latest_year]

    total_assets = balance_sheet.loc["Total Assets", latest_year]
    total_liabilities  =balance_sheet.loc["Total Liabilities Net Minority Interest", latest_year]

    #Ratios
    profit_margin = net_income / total_revenue
    roa = net_income / total_assets
    debt_to_assets = total_liabilities / total_assets

    # Growth
    prev_revenue = income_stmt.loc["Total Revenue", previous_year]
    revenue_growth = (total_revenue - prev_revenue) / prev_revenue

    return {
        "profit_margin": profit_margin,
        "roa": roa,
        "debt_to_assets": debt_to_assets,
        "revenue_growth": revenue_growth
    }

def interpret_ratios(ratios):
    interpretation = {}

    #Profitability
    if ratios["profit_margin"] < 0:
        interpretation["profitability"] = "Operating at a loss"
    elif ratios["profit_margin"] > 0.3:
        interpretation["profitability"] = "Strong profitability"
    elif ratios["profit_margin"] > 0.15:
        interpretation["profitability"] = "Moderate profitability"
    else:
        interpretation["profitability"] = "Weak profitability"

    #Asset efficiency
    if ratios["roa"] < 0:
        interpretation["asset_efficiency"] = "Negative return on assets"
    elif ratios["roa"] > 0.2:
        interpretation["asset_efficiency"] = "Highly efficient asset utilization"
    elif ratios["roa"] > 0.1:
        interpretation["asset_efficiency"] = "Moderate asset utilization"
    else:
        interpretation["asset_efficiency"] = "Low asset efficiency"

    # Leverage
    if ratios["debt_to_assets"] < 0.3:
        interpretation["leverage"] = "Low financial risk"
    elif ratios["debt_to_assets"] < 0.6:
        interpretation["leverage"] = "Moderate financial risk"
    else:
        interpretation["leverage"] = "High financial risk"

    # Growth
    if ratios["revenue_growth"] > 0.2:
        interpretation["growth"] = "High growth"
    elif ratios["revenue_growth"] > 0:
        interpretation["growth"] = "Stable growth"
    else:
        interpretation["growth"] = "Revenue contraction"

    return interpretation

def score_company (ratios):
    scores = {}

    #Profitability Score
    pm = ratios["profit_margin"]
    if pm < 0:
        scores["profitability_score"] = 0
    elif pm < 0.1:
        scores["profitability_score"] = 3
    elif pm < 0.2:
        scores["profitability_score"] = 6
    elif pm < 0.3:
        scores["profitability_score"] = 8
    else:
        scores["profitability_score"] = 10

    # Efficiency Score (ROA)
    roa = ratios["roa"]
    if roa < 0:
        scores["efficiency_score"] = 0
    elif roa < 0.05:
        scores["efficiency_score"] = 3
    elif roa < 0.15:
        scores["efficiency_score"] = 6
    elif roa < 0.25:
        scores["efficiency_score"] = 8
    else:
        scores["efficiency_score"] = 10

    # Leverage Score (lower debt = better)
    dta = ratios["debt_to_assets"]
    if dta > 0.7:
        scores["leverage_score"] = 0
    elif dta > 0.5:
        scores["leverage_score"] = 4
    elif dta > 0.3:
        scores["leverage_score"] = 7
    else:
        scores["leverage_score"] = 10

    # Growth Score
    growth = ratios["revenue_growth"]
    if growth < 0:
        scores["growth_score"] = 0
    elif growth < 0.05:
        scores["growth_score"] = 4
    elif growth < 0.2:
        scores["growth_score"] = 7
    else:
        scores["growth_score"] = 10

    # Weighted overall score
    weights = {
        "profitability_score": 0.30,
        "efficiency_score": 0.25,
        "growth_score": 0.25,
        "leverage_score": 0.20
    }

    weighted_total = 0
    for key in weights:
        weighted_total += scores[key] * weights[key]

    scores["overall_score"] = round(weighted_total, 2)
    return scores