from data.financial_data import get_basic_info

def main():
    ticker = input("Enter ticker symbol: ").upper()
    data = get_basic_info(ticker)
    
    print("\nCompany Information:")
    for key, value in data.items():
        if value is None:
            print(f"{key}: Data not available")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()