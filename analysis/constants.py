currencies_futures = {
    "AUD": {"ticker": "6A=F", "name": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"},
    "GBP": {"ticker": "6B=F", "name": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"},
    "CAD": {"ticker": "6C=F", "name": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"},
    "EUR": {"ticker": "6E=F", "name": "EURO FX - CHICAGO MERCANTILE EXCHANGE"},
    "JPY": {"ticker": "6J=F", "name": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE"},
    "CHF": {"ticker": "6S=F", "name": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE"},
    "USD": {"ticker": "DX=F", "name": "USD INDEX - ICE FUTURES U.S."},
}

# asset_list = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF"]
asset_list = ["CAD", "CHF"]
# asset_list = ["USD"]

report_types = {
    # "Disaggregated": {"type": "disaggregated_futopt", "filename": "c_year"},
    "TFF": {"type": "traders_in_financial_futures_futopt", "filename": "FinComYY"},
}

operators = {
    # "Managed money": "MM",
    "Asset Manager": "AM",
    "Leveraged Money": "LM",
}
