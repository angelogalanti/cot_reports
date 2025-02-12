import pandas as pd


class DataProcessor:
    def __init__(self, cot_data, price_data):
        self.cot_data = cot_data
        self.price_data = price_data

    def merge_data(self) -> pd.DataFrame:
        # First ensure the index of both dataframes is a datetime index
        self.cot_data.index = pd.to_datetime(self.cot_data.index)
        self.price_data.index = pd.to_datetime(self.price_data.index)

        # # drop all except AM_net from df_asset
        # self.cot_data.drop(columns=["AM_L", "AM_S", "Ch_AM_L", "Ch_AM_S"], inplace=True)

        # add df_asset to data dataframe, forwards fill the NaN values
        self.price_data = self.price_data.join(self.cot_data, how="left")
        # data.fillna(method='ffill', inplace=True)
        self.price_data.ffill(inplace=True)
        # drop rows with NaN values
        self.price_data.dropna(inplace=True)
        return self.price_data

    def shift_cot_data(self, shift_days=7):
        data_shifted = self.price_data.copy()
        # shift the AM_Net column by 7 days
        data_shifted["AM_Net"] = data_shifted["AM_Net"].shift(-shift_days)
        # drop rows with NaN values
        data_shifted.dropna(inplace=True)
        return data_shifted
