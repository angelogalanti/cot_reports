from pathlib import Path

from analysis.data_loader import DataLoader
from analysis.yahoo_finance_downloader import YahooFinanceDownloader
from analysis.data_processor import DataProcessor
from analysis.plotter import Plotter
from analysis.constants import currencies_futures, asset_list, operators

year = 2025
operator = operators["Asset Manager"]

for asset in asset_list:
    ticker = currencies_futures[asset]["ticker"]
    # Define the path relative to the current file
    filename = f"{year}FinComYY.txt"
    data_folder = Path(__file__).parent / "data"
    plot_folder = Path(__file__).parent / "plots"
    data_path = data_folder / filename

    # Load and preprocess COT data
    data_loader = DataLoader(filename=data_path)
    df_asset = data_loader.load_and_preprocess(currencies_futures, asset)

    # Plot COT data
    plotter = Plotter(plot_folder, asset)
    plotter.plot_asset_manager_positions(df_asset)

    # Download and preprocess price data
    yahoo_downloader = YahooFinanceDownloader(asset, ticker, year)
    price_data = yahoo_downloader.load_and_preprocess()

    # Process data
    data_processor = DataProcessor(df_asset, price_data)
    merged_data = data_processor.merge_data()

    # Plot price data
    plotter.plot_price_and_cot(merged_data)

    # Shift COT data and plot
    if False:
        shifted_data = data_processor.shift_cot_data(shift_days=7)
        plotter.plot_price_and_cot(shifted_data, title="(COT Data Shifted by 7 Days)")

    if False:
        plotter.plot_operator(merged_data, df_asset, operator=operator, title=asset, show_plot=False)

    plotter.plot_operators(merged_data, df_asset, operators, title=asset, show_plot=False)
