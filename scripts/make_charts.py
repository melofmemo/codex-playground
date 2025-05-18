import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def main():
    df = pd.read_csv("data/tsla_prices.csv", parse_dates=["Date"])
    df.set_index("Date", inplace=True)
    df.sort_index(inplace=True)

    df["SMA7"] = df["Close"].rolling(window=7).mean()
    df["SMA30"] = df["Close"].rolling(window=30).mean()

    last_six_months = df.tail(180)

    plt.figure(figsize=(10, 6))
    plt.plot(last_six_months.index, last_six_months["Close"], label="Close")
    plt.plot(last_six_months.index, last_six_months["SMA7"], label="SMA 7")
    plt.plot(last_six_months.index, last_six_months["SMA30"], label="SMA 30")
    plt.title("Tesla Stock Price - Last 6 Months")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()

    Path("site_src/assets").mkdir(parents=True, exist_ok=True)
    plt.savefig("site_src/assets/price_sma.png", dpi=150)


if __name__ == "__main__":
    main()
