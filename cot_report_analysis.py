from pathlib import Path

import pandas as pd

import cot_reports as cot

from analysis.data_loader import DataLoader
from analysis.yahoo_finance_downloader import YahooFinanceDownloader
from analysis.data_processor import DataProcessor
from analysis.plotter import Plotter
from analysis.constants import currencies_futures, asset_list, operators, report_types, operator_name

single_year = False
plot_operator = True
plot_all = False
save_df = True

begin_year = 2024
end_year = 2025
operator = operators[operator_name]
data_folder = Path(__file__).parent / "data"
cot_folder = data_folder / "cot"
if single_year:
    price_folder = data_folder / "price" / str(end_year)
else:
    price_folder = data_folder / "price" / "current"
plot_folder = Path(__file__).parent / "plots"
output_folder = Path(__file__).parent / "output"
df = pd.DataFrame()
all_df = pd.DataFrame()


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    # Remove leading/trailing whitespace from columns
    df.columns = df.columns.str.strip().str.replace('"', "")
    # Optionally, remove quotes from string columns and convert numbers
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip().str.replace('"', "")
    return df


def download_cot_report(begin_year: int, end_year: int, single: bool, cot_folder: Path, report: dict) -> pd.DataFrame:
    report_type = report_types[report]["type"]
    report_filename = report_types[report]["filename"]

    filename_single_year = f"{end_year}{report_filename}.txt"
    filename_multi_year = f"{begin_year}_{end_year}{report_filename}.txt"
    data_path_single_year = cot_folder / filename_single_year
    data_path_multi_year = cot_folder / filename_multi_year

    if single:
        if data_path_single_year.exists():
            print(f"Data already exists for {end_year}.")
            # df = pd.read_csv(data_path_single_year, skipinitialspace=True)
            df = pd.read_csv(data_path_single_year, skipinitialspace=True, low_memory=False)
            return normalize_df(df)
        print(f"Downloading {report_type} report for {end_year}")
        df = cot.cot_year(year=end_year, cot_report_type=report_type)
        df.to_csv(data_path_single_year, index=False)
        return df

    if data_path_multi_year.exists():
        print(f"Data already exists for {begin_year} to {end_year}.")
        # df = pd.read_csv(data_path_multi_year, skipinitialspace=True)
        df = pd.read_csv(data_path_multi_year, skipinitialspace=True, low_memory=False)
        return normalize_df(df)

    df_list = []
    for i in range(begin_year, end_year + 1):
        yearly_path = cot_folder / f"{i}{report_filename}.txt"
        if yearly_path.exists():
            print(f"Data already exists for {i}.")
            # yearly_df = pd.read_csv(yearly_path, skipinitialspace=True)
            yearly_df = pd.read_csv(yearly_path, skipinitialspace=True, low_memory=False)
            yearly_df = normalize_df(yearly_df)
        else:
            print(f"Downloading {report_type} report for {i}")
            yearly_df = cot.cot_year(year=i, cot_report_type=report_type)
            yearly_df.to_csv(yearly_path, index=False)
        df_list.append(yearly_df)

    df = pd.concat(df_list, ignore_index=True)
    df.to_csv(data_path_multi_year, index=False)
    return df


# check if folder exists
if not data_folder.exists():
    data_folder.mkdir()
if not plot_folder.exists():
    plot_folder.mkdir()
if not output_folder.exists():
    output_folder.mkdir()

for report in report_types:
    print(f"Processing {report} report")
    df = download_cot_report(begin_year, end_year, single_year, cot_folder, report)

    for asset in asset_list:
        print(f"Processing {asset}")
        ticker = currencies_futures[asset]["ticker"]

        # Load and preprocess COT data
        data_loader = DataLoader(df=df)
        df_asset = data_loader.load_and_preprocess(currencies_futures, asset, report)

        # Download and preprocess price data
        if single_year:
            yahoo_downloader = YahooFinanceDownloader(
                asset, ticker, price_folder, begin_year=end_year, end_year=end_year
            )
        else:
            yahoo_downloader = YahooFinanceDownloader(
                asset, ticker, price_folder, begin_year=begin_year, end_year=end_year
            )

        price_data = yahoo_downloader.load_and_preprocess()

        # Process data
        data_processor = DataProcessor(df_asset, price_data)
        merged_data = data_processor.merge_data()

        # Plot
        plotter = Plotter(plot_folder, asset)

        if plot_operator:
            plotter.plot_operator(merged_data, df_asset, operator=operator, title=asset, show_plot=False)

        if plot_all:
            plotter.plot_operators(merged_data, df_asset, operators, title=asset, show_plot=False)

        if save_df:
            # Keep columns: Close, AM_Net
            merged_data = merged_data[["Close", f"{operator}_Net"]].copy()

            # Convert AM_Net to standard NumPy int64 type (if no NAs are expected)
            merged_data.loc[:, f"{operator}_Net"] = merged_data[f"{operator}_Net"].astype("int64")

            # Write CSV with Close formatted to 5 decimals; AM_Net will now be written as an integer.
            merged_data.to_csv(output_folder / f"{asset}_{operator_name}.csv", index=True)

            # Merge all the dataframes into one
            merged_data = merged_data.rename(columns={"Close": asset, f"{operator}_Net": f"{asset}_{operator}_Net"})
            if all_df.empty:
                all_df = merged_data
            else:
                all_df = all_df.merge(merged_data, how="outer", left_index=True, right_index=True)

    if save_df:
        all_df.to_csv(output_folder / f"all_cot_{report}_{operator_name}.csv", index=True)
