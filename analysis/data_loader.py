import pandas as pd
import numpy as np
from .constants import currencies_futures


class DataLoader:
    def __init__(self, filename="FinFutYY.txt"):
        self.filename = filename
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.filename)
        return self

    def drop_columns_with_patterns(self, patterns):
        """Drop columns that contain any of the specified patterns."""
        for col in self.df.columns:
            for pattern in patterns:
                if pattern in col and col in self.df.columns:
                    self.df.drop(col, axis=1, inplace=True)
        return self

    def rename_columns(self, rename_mapping):
        """Rename columns based on a list of dictionaries."""
        for mapping in rename_mapping:
            self.df.rename(columns=mapping, inplace=True)
        return self

    def convert_datatypes(self):
        """Convert date column to datetime and numeric columns to float."""
        self.df["Date"] = pd.to_datetime(self.df["Date"]).dt.date

        for col in self.df.columns:
            if col not in ["Market", "Date"]:
                self.df[col] = self.df[col].replace(".", np.nan)
                self.df[col] = self.df[col].astype(float)
        return self

    def preprocess_cot_data(self):
        contains = [
            "Conc_",
            "Traders",
            "Dealer",
            "Other_Rept",
            "NonRept",
            "Pct_of_",
            "CFTC_",
            "As_of_Date_",
            "Spread_",
            "Contract_Units",
            "FutOnly_or_Combined",
            "Open_Interest_",
        ]  # , 'Positions_']

        names = [
            {"Market_and_Exchange_Names": "Market"},
            {"Report_Date_as_YYYY-MM-DD": "Date"},
            {"Asset_Mgr_Positions_Long_All": "AM_L"},
            {"Asset_Mgr_Positions_Short_All": "AM_S"},
            {"Lev_Money_Positions_Long_All": "LM_L"},
            {"Lev_Money_Positions_Short_All": "LM_S"},
            {"Tot_Rept_Positions_Long_All": "TR_L"},
            {"Tot_Rept_Positions_Short_All": "TR_S"},
            {"Change_in_Asset_Mgr_Long_All": "Ch_AM_L"},
            {"Change_in_Asset_Mgr_Short_All": "Ch_AM_S"},
            {"Change_in_Lev_Money_Long_All": "Ch_LM_L"},
            {"Change_in_Lev_Money_Short_All": "Ch_LM_S"},
            {"Change_in_Tot_Rept_Long_All": "Ch_TR_L"},
            {"Change_in_Tot_Rept_Short_All": "Ch_TR_S"},
        ]

        self.drop_columns_with_patterns(contains)
        self.rename_columns(names)
        self.convert_datatypes()

        return self

    def filter_currency_data(self, currencies_futures):
        # Rename the markets to the currency codes
        for key, value in currencies_futures.items():
            self.df["Market"] = self.df["Market"].replace(value["name"], key)

        # Keep only the rows with currency futures
        self.df = self.df[self.df["Market"].isin(currencies_futures.keys())]
        return self

    def get_asset_data(self, asset):
        # create a copy of the dataframe for the asset
        df_asset = self.df.loc[self.df["Market"] == asset].copy()

        # sort by date
        df_asset.sort_values(by="Date", inplace=True)

        # use date as index
        df_asset.set_index("Date", inplace=True)

        # keep only Asset Manager data: columns 'AM_L', 'AM_S', 'Ch_AM_L', 'Ch_AM_S'
        df_asset = df_asset[["AM_L", "AM_S", "Ch_AM_L", "Ch_AM_S"]]

        # add a column 'AM_Net' that is the difference between 'AM_L' and 'AM_S'
        df_asset["AM_Net"] = df_asset["AM_L"] - df_asset["AM_S"]
        return df_asset

    def load_and_preprocess(self, currencies_futures, asset):
        self.load_data().preprocess_cot_data().filter_currency_data(currencies_futures)
        df_asset = self.get_asset_data(asset)
        return df_asset
