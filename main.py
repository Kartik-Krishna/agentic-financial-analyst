from data.financial_data import get_basic_info, get_financial_statements

def main():
    ticker = input("Enter ticker symbol: ").upper()
    
    #Basic Info
    data = get_basic_info(ticker)
    
    print("\nCompany Information:")
    for key, value in data.items():
        if value is None:
            print(f"{key}: Data not available")
        else:
            print(f"{key}: {value}")
    
    #Financial Statements
    income_stmt, balance_sheet, cash_flow = get_financial_statements(ticker)

    print("\nAvailable Income Statement Years:")
    print(income_stmt.columns)

    print("\nAvailable Balance Sheet Years:")
    print(balance_sheet.columns)

    latest_year = income_stmt.columns[0]

    print(f"\nLatest Financial Year: {latest_year.date()}")

    # Income Statement Metrics
    total_revenue = income_stmt.loc["Total Revenue", latest_year]
    net_income = income_stmt.loc["Net Income", latest_year]

    # Balance Sheet Metrics
    total_assets = balance_sheet.loc["Total Assets", latest_year]
    total_liabilities = balance_sheet.loc["Total Liabilities Net Minority Interest", latest_year]

    print("\nKey Metrics:")
    print("Total Revenue:", total_revenue)
    print("Net Income:", net_income)
    print("Total Assets:", total_assets)
    print("Total Liabilities:", total_liabilities)

if __name__ == "__main__":
    main()