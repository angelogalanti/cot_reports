from cot_reports.data_loader import DataLoader
from cot_reports.yahoo_finance_downloader import YahooFinanceDownloader
from cot_reports.data_processor import DataProcessor
from cot_reports.plotter import Plotter
from cot_reports.constants import currencies_futures

asset = "USD"
ticker = currencies_futures[asset]["ticker"]
year = 2020

# Load and preprocess COT data
data_loader = DataLoader()
df_asset = data_loader.load_and_preprocess(currencies_futures, asset)

# Plot COT data
plotter = Plotter(asset)
plotter.plot_asset_manager_positions(df_asset)

# Download and preprocess price data
yahoo_downloader = YahooFinanceDownloader(ticker, year)
price_data = yahoo_downloader.load_and_preprocess()

# Process data
data_processor = DataProcessor(df_asset, price_data)
merged_data = data_processor.merge_data()

# Plot price data
plotter.plot_price_data(merged_data)
plotter.plot_price_and_cot(merged_data)

# Shift COT data and plot
shifted_data = data_processor.shift_cot_data(shift_days=7)
plotter.plot_price_and_cot(shifted_data, title="(COT Data Shifted by 7 Days)")
