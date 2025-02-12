import os

from matplotlib.axis import Axis
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Plotter:
    def __init__(self, plot_folder, asset):
        self.plot_folder = plot_folder
        self.asset = asset

    def plot_asset_manager_positions(self, df_asset, show_plot=False):
        plt.figure(figsize=(10, 5))
        plt.plot(df_asset.index, df_asset["AM_L"], label="AM_L")
        plt.plot(df_asset.index, df_asset["AM_S"], label="AM_S")
        plt.plot(df_asset.index, df_asset["AM_Net"], label="AM_Net")
        plt.title("Asset Manager Positions")
        plt.xlabel("Date")
        plt.ylabel("Position")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(self.plot_folder, f"{self.asset}_asset_manager_positions.png"))
        if show_plot:
            plt.show()
        plt.close()

        # in a separate plot, plot the changes in 'AM_L' and 'AM_S': Ch_AM_L and Ch_AM_S
        plt.figure(figsize=(10, 5))
        plt.plot(df_asset.index, df_asset["Ch_AM_L"], label="Ch_AM_L")
        plt.plot(df_asset.index, df_asset["Ch_AM_S"], label="Ch_AM_S")
        plt.title("Change in Asset Manager Positions")
        plt.xlabel("Date")
        plt.ylabel("Change in Position")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(self.plot_folder, f"{self.asset}_change_in_asset_manager_positions.png"))
        if show_plot:
            plt.show()
        plt.close()

    def plot_price_data(self, data, show_plot=False):
        # plot the data
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data["Close"], label="Close")
        plt.title(f"{self.asset} Close Price and Asset Manager Net Positions")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(self.plot_folder, f"{self.asset}_close_price.png"))
        if show_plot:
            plt.show()
        plt.close()
        # plot asset manager net positions
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data["AM_Net"], label="AM_Net")
        plt.title(f"{self.asset} Asset Manager Net Positions")
        plt.xlabel("Date")
        plt.ylabel("Position")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(self.plot_folder, f"{self.asset}_asset_manager_net_positions.png"))
        if show_plot:
            plt.show()
        plt.close()

    def plot_price_and_cot(self, data, title="", show_plot=False):
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
        plt.savefig(os.path.join(self.plot_folder, f"{self.asset}_price_and_cot_{title}.png"))
        if show_plot:
            plt.show()
        plt.close()

    def plot_operator(self, data, df_asset, operator, title="", show_plot=False):
        # create a plot with 3 subplots:
        # in the first plot the operator positions
        # in the second plot the change in operator positions
        # in the third plot the price and operator net positions

        fig, axs = plt.subplots(3, 1, figsize=(20, 15))
        fig.suptitle(title)

        # First subplot: Operator Positions
        axs[0].plot(df_asset.index, df_asset[f"{operator}_L"], label=f"{operator}_L")
        axs[0].plot(df_asset.index, df_asset[f"{operator}_S"], label=f"{operator}_S")
        axs[0].plot(df_asset.index, df_asset[f"{operator}_Net"], label=f"{operator}_Net")
        axs[0].set_title(f"{operator} Positions")
        axs[0].set_xlabel("Date")
        axs[0].set_ylabel("Position")
        axs[0].legend()
        axs[0].grid()

        # Second subplot: Change in Operator Positions
        axs[1].plot(df_asset.index, df_asset[f"Ch_{operator}_L"], label=f"Ch_{operator}_L")
        axs[1].plot(df_asset.index, df_asset[f"Ch_{operator}_S"], label=f"Ch_{operator}_S")
        axs[1].set_title(f"Change in {operator} Positions")
        axs[1].set_xlabel("Date")
        axs[1].set_ylabel("Change in Position")
        axs[1].legend()
        axs[1].grid()

        # Third subplot: Price and Operator Net Positions
        ax2 = axs[2].twinx()
        color = "tab:red"
        axs[2].set_xlabel("Date")
        axs[2].set_ylabel("Price", color=color)
        axs[2].plot(data.index, data["Close"], color=color, label="Close")
        axs[2].tick_params(axis="y", labelcolor=color)
        axs[2].legend(loc="upper left")
        axs[2].set_title(f"{self.asset} Close Price and {operator} Net Positions")
        axs[2].grid()
        color = "tab:blue"
        ax2.set_ylabel(f"{operator}_Net", color=color)
        ax2.plot(data.index, data[f"{operator}_Net"], color=color, label=f"{operator}_Net")
        ax2.tick_params(axis="y", labelcolor=color)
        ax2.legend(loc="upper right")

        fig.tight_layout()
        plt.savefig(os.path.join(self.plot_folder, f"{self.asset}_{operator}_positions.png"))
        if show_plot:
            plt.show()
        plt.close()

    def plot_operators(self, data, df_asset, operators, title="", show_plot=False):
        # create a plot with 2 columns for each operator and 3 rows for each operator:
        # in the first plot the operator positions
        # in the second plot the change in operator positions
        # in the third plot the price and operator net positions

        num_operators = len(operators)

        fig, axs = plt.subplots(3, num_operators, figsize=(20 * num_operators, 15))
        fig.suptitle(title)

        for i, operator in enumerate(operators):
            operator = operators[operator]
            # First subplot: Operator Positions
            axs[0, i].plot(df_asset.index, df_asset[f"{operator}_L"], label=f"{operator}_L")
            axs[0, i].plot(df_asset.index, df_asset[f"{operator}_S"], label=f"{operator}_S")
            axs[0, i].plot(df_asset.index, df_asset[f"{operator}_Net"], label=f"{operator}_Net")
            axs[0, i].set_title(f"{operator} Positions")
            axs[0, i].set_xlabel("Date")
            axs[0, i].set_ylabel("Position")
            axs[0, i].legend()
            axs[0, i].grid()

            # Second subplot: Change in Operator Positions
            axs[1, i].plot(df_asset.index, df_asset[f"Ch_{operator}_L"], label=f"Ch_{operator}_L")
            axs[1, i].plot(df_asset.index, df_asset[f"Ch_{operator}_S"], label=f"Ch_{operator}_S")
            axs[1, i].set_title(f"Change in {operator} Positions")
            axs[1, i].set_xlabel("Date")
            axs[1, i].set_ylabel("Change in Position")
            axs[1, i].legend()
            axs[1, i].grid()

            # Third subplot: Price and Operator Net Positions
            ax2: Axis = axs[2, i].twinx()
            color = "tab:red"
            axs[2, i].set_xlabel("Date")
            axs[2, i].set_ylabel("Price", color=color)
            axs[2, i].plot(data.index, data["Close"], color=color, label="Close")
            axs[2, i].tick_params(axis="y", labelcolor=color)
            axs[2, i].legend(loc="upper left")
            axs[2, i].set_title(f"{self.asset} Close Price and {operator} Net Positions")
            axs[2, i].grid()
            color = "tab:blue"
            ax2.set_ylabel(f"{operator}_Net", color=color)
            ax2.plot(data.index, data[f"{operator}_Net"], color=color, label=f"{operator}_Net")
            ax2.tick_params(axis="y", labelcolor=color)
            ax2.legend(loc="upper right")

        if False:
            fig.tight_layout(rect=[0, 0.03, 1, 0.95])
            # Rotate x-axis tick labels for all subplots to reduce tightness
            for ax in axs.flat:
                ax.xaxis.set_major_locator(mdates.WeekdayLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
            plt.setp(ax.get_xticklabels(), rotation=45)
        plt.savefig(os.path.join(self.plot_folder, f"{self.asset}_operators_positions.png"))
        if show_plot:
            plt.show()
        plt.close()
