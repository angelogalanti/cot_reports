import matplotlib.pyplot as plt


class Plotter:
    def __init__(self, asset):
        self.asset = asset

    def plot_asset_manager_positions(self, df_asset):
        plt.figure(figsize=(10, 5))
        plt.plot(df_asset.index, df_asset["AM_L"], label="AM_L")
        plt.plot(df_asset.index, df_asset["AM_S"], label="AM_S")
        plt.plot(df_asset.index, df_asset["AM_Net"], label="AM_Net")
        plt.title("Asset Manager Positions")
        plt.xlabel("Date")
        plt.ylabel("Position")
        plt.legend()
        plt.grid()
        plt.show()

        # in a separate plot, plot the changes in 'AM_L' and 'AM_S': Ch_AM_L and Ch_AM_S
        plt.figure(figsize=(10, 5))
        plt.plot(df_asset.index, df_asset["Ch_AM_L"], label="Ch_AM_L")
        plt.plot(df_asset.index, df_asset["Ch_AM_S"], label="Ch_AM_S")
        plt.title("Change in Asset Manager Positions")
        plt.xlabel("Date")
        plt.ylabel("Change in Position")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_price_data(self, data):
        # plot the data
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data["Close"], label="Close")
        plt.title(f"{self.asset} Close Price and Asset Manager Net Positions")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.show()
        # plot asset manager net positions
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data["AM_Net"], label="AM_Net")
        plt.title(f"{self.asset} Asset Manager Net Positions")
        plt.xlabel("Date")
        plt.ylabel("Position")
        plt.legend()
        plt.grid()
        plt.show()

    def plot_price_and_cot(self, data, title=""):
        # plot both on the same plot with 2 y-axes
        fig, ax1 = plt.subplots(figsize=(10, 5))
        color = "tab:red"
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price", color=color)
        ax1.plot(data.index, data["Close"], color=color, label="Close")
        ax1.tick_params(axis="y", labelcolor=color)
        ax1.legend(loc="upper left")
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = "tab:blue"
        ax2.set_ylabel("AM_Net", color=color)  # we already handled the x-label with ax1
        ax2.plot(data.index, data["AM_Net"], color=color, label="AM_Net")
        ax2.tick_params(axis="y", labelcolor=color)
        ax2.legend(loc="upper right")
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title(f"{self.asset} Close Price and Asset Manager Net Positions {title}")
        plt.show()
