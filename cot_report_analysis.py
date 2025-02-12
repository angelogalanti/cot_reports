from pathlib import Path

import pandas as pd

import cot_reports as cot

from analysis.data_loader import DataLoader
from analysis.yahoo_finance_downloader import YahooFinanceDownloader
from analysis.data_processor import DataProcessor
from analysis.plotter import Plotter
from analysis.constants import currencies_futures, asset_list, operators, report_types

single_year = False
year = 2025
begin_year = 2024
end_year = 2025
operator = operators["Asset Manager"]
data_folder = Path(__file__).parent / "data"
plot_folder = Path(__file__).parent / "plots"
df = pd.DataFrame()


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # Remove leading/trailing whitespace from columns
    df.columns = df.columns.str.strip().str.replace('"', "")
    # Optionally, remove quotes from string columns and convert numbers
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip().str.replace('"', "")
    return df


def download_cot_report(begin_year: int, end_year: int, single: bool, data_folder: Path, report: str) -> pd.DataFrame:
    report_type = report_types[report]["type"]
    report_filename = report_types[report]["filename"]

    filename_single_year = f"{end_year}{report_filename}.txt"
    filename_multi_year = f"{begin_year}_{end_year}{report_filename}.txt"
    data_path_single_year = data_folder / filename_single_year
    data_path_multi_year = data_folder / filename_multi_year

    if single:
        if data_path_single_year.exists():
            print(f"Data already exists for {end_year}.")
            df = pd.read_csv(data_path_single_year, skipinitialspace=True)
            return normalize_df(df)
        print(f"Downloading {report_type} report for {end_year}")
        df = cot.cot_year(year=end_year, cot_report_type=report_type)
        df.to_csv(data_path_single_year, index=False)
        return df

    if data_path_multi_year.exists():
        print(f"Data already exists for {begin_year} to {end_year}.")
        df = pd.read_csv(data_path_multi_year, skipinitialspace=True)
        return normalize_df(df)

    df_list = []
    for i in range(begin_year, end_year + 1):
        yearly_path = data_folder / f"{i}{report_filename}.txt"
        if yearly_path.exists():
            print(f"Data already exists for {i}.")
            yearly_df = pd.read_csv(yearly_path, skipinitialspace=True)
            yearly_df = normalize_df(yearly_df)
        else:
            print(f"Downloading {report_type} report for {i}")
            yearly_df = cot.cot_year(year=i, cot_report_type=report_type)
            yearly_df.to_csv(yearly_path, index=False)
        df_list.append(yearly_df)

    df = pd.concat(df_list, ignore_index=True)
    df.to_csv(data_path_multi_year, index=False)
    return df


for report in report_types:
    df = download_cot_report(begin_year, end_year, single_year, data_folder, report)

    for asset in asset_list:
        ticker = currencies_futures[asset]["ticker"]

        # Load and preprocess COT data
        data_loader = DataLoader(df=df)
        df_asset = data_loader.load_and_preprocess(currencies_futures, asset)

        # Download and preprocess price data
        yahoo_downloader = YahooFinanceDownloader(asset, ticker, begin_year=begin_year, end_year=end_year)
        price_data = yahoo_downloader.load_and_preprocess()

        # Process data
        data_processor = DataProcessor(df_asset, price_data)
        merged_data = data_processor.merge_data()

        # Plot
        plotter = Plotter(plot_folder, asset)

        # Plot COT data
        if False:
            plotter.plot_asset_manager_positions(df_asset)

        # Plot price data
        if False:
            plotter.plot_price_and_cot(merged_data)

        # Shift COT data and plot
        if False:
            shifted_data = data_processor.shift_cot_data(shift_days=7)
            plotter.plot_price_and_cot(shifted_data, title="(COT Data Shifted by 7 Days)")

        if False:
            plotter.plot_operator(merged_data, df_asset, operator=operator, title=asset, show_plot=False)

        # if False:
        plotter.plot_operators(merged_data, df_asset, operators, title=asset, show_plot=False)
