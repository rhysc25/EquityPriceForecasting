import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from GlobalVariables import marketDataFrame, rowsTotal
import matplotlib.dates as mdates

def plotWithIndicators(parameters, show_ma=None, show_rsi=False):
    # show_ma : list or None
    # show_rsi: bool

    timeArray = marketDataFrame["t"].to_numpy()
    vwArray = marketDataFrame["vw"].to_numpy()

    # Setup subplots
    if show_rsi:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                       gridspec_kw={'height_ratios': [3, 1]})
    else:
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax2 = None

    # Plot main price chart
    ax1.plot(timeArray, vwArray, label='VWAP', color='black')

    if show_ma:
        for ma in show_ma:
            if ma in marketDataFrame.columns:
                ax1.plot(timeArray, marketDataFrame[ma], label=ma.upper())
            else:
                print(f"Warning: '{ma}' not in DataFrame columns")

    symbol = parameters["symbols"]
    title = symbol + " Price"
    ax1.set_title(title)

    if parameters["currency"] == "":
        units = "USD"
    else:
        units = parameters["currency"]
    ax1.set_ylabel("Price /" + units)

    ax1.grid(True)
    ax1.legend()
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=10))

    # 🔹 Format x-axis as YYYY-MM-DD
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Plot RSI below if requested
    if show_rsi:
        if 'rsi' not in marketDataFrame.columns:
            print("Warning: 'rsi' column not found")
        else:
            ax2.plot(timeArray, marketDataFrame['rsi'], label='RSI', color='purple')
            ax2.set_ylabel("RSI")
            ax2.grid(True)
            ax2.axhline(70, color='red', linestyle='--', linewidth=0.8)  # overbought line
            ax2.axhline(30, color='green', linestyle='--', linewidth=0.8)  # oversold line
            ax2.legend()
            # 🔹 also format RSI subplot x-axis
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()