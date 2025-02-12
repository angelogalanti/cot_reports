currencies_futures = {
    "AUD": {"ticker": "6A=F", "name": "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"},
    "GBP": {"ticker": "6B=F", "name": "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"},
    "CAD": {"ticker": "6C=F", "name": "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"},
    "EUR": {"ticker": "6E=F", "name": "EURO FX - CHICAGO MERCANTILE EXCHANGE"},
    "JPY": {"ticker": "6J=F", "name": "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE"},
    "CHF": {"ticker": "6S=F", "name": "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE"},
    "NZD": {"ticker": "6S=F", "name": "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE"},
    "USD": {"ticker": "DX=F", "name": "USD INDEX - ICE FUTURES U.S."},
    "ZAR": {"ticker": "6Z=F", "name": "SO AFRICAN RAND - CHICAGO MERCANTILE EXCHANGE"},
    "BRL": {"ticker": "6L=F", "name": "BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE"},
    "MXN": {"ticker": "6M=F", "name": "MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE"},
    "GC": {"ticker": "GC=F", "name": "GOLD - COMMODITY EXCHANGE INC."},
    "SI": {"ticker": "SI=F", "name": "SILVER - COMMODITY EXCHANGE INC."},
    "HG": {"ticker": "HG=F", "name": "COPPER-#1 - COMMODITY EXCHANGE INC."},
    "CL": {"ticker": "CL=F", "name": "WTI FINANCIAL CRUDE OIL - NEW YORK MERCANTILE EXCHANGE"},
}

# asset_list = ["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "NZD"]
asset_list = ["GC", "SI", "HG", "CL"]
# asset_list = ["GC"]
# asset_list = ["USD"]

report_types = {
    # "TFF": {"type": "traders_in_financial_futures_futopt", "filename": "FinComYY"},
    "DIS": {"type": "disaggregated_futopt", "filename": "c_year"},
    # "CITS": {"type": "supplemental_futopt", "filename": "dea_cit_txt_"},
}

operators = {
    "Total Reportables": "TR",
    "Asset Manager": "AM",
    "Leveraged Money": "LM",
}
