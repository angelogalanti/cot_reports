import yfinance as yf
import pandas as pd
import os
from pathlib import Path


class YahooFinanceDownloader:
    def __init__(self, asset, ticker, begin_year, end_year):
        self.asset = asset
        self.ticker = ticker
        self.begin_year = begin_year
        self.end_year = end_year
        self.filename = Path(__file__).parent.parent / "data" / f"{asset}_{begin_year}_{end_year}_daily_data.csv"
        self.data = None

    def download_data(self):
        if os.path.exists(self.filename):
            print(f"The file {self.filename} already exists.")
        else:
            # get the data
            self.data = yf.download(self.ticker, start=f"{self.begin_year}-01-01", end=f"{self.end_year}-12-31")
            # save the data to a file
            self.data.to_csv(self.filename)
            print(f"The file {self.filename} has been created.")
        return self

    def load_data(self):
        # read the data from the file
        self.data = pd.read_csv(self.filename)
        return self

    def preprocess_price_data(self):
        # drop the first 2 rows
        self.data = self.data.iloc[2:]
        # reset the index
        self.data = self.data.reset_index(drop=True)
        # rename Price to Date
        self.data.rename(columns={"Price": "Date"}, inplace=True)
        # keep only the columns Date and Close
        self.data = self.data[["Date", "Close"]]
        # use Date as index
        self.data.set_index("Date", inplace=True)
        # Close as float
        self.data["Close"] = self.data["Close"].astype(float)
        return self

    def load_and_preprocess(self):
        self.download_data()
        self.load_data()
        self.preprocess_price_data()
        return self.data
