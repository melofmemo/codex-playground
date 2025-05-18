import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv('data/tsla_prices.csv', parse_dates=['Date'], index_col='Date')
    df['Close'] = pd.to_numeric(df['Close'].str.replace(',', ''), errors='coerce')
    df['SMA7'] = df['Close'].rolling(window=7).mean()
    df['SMA30'] = df['Close'].rolling(window=30).mean()

    last_date = df.index.max()
    start_date = last_date - pd.DateOffset(months=6)
    df_last = df.loc[start_date:]

    plt.figure(figsize=(10, 6))
    plt.plot(df_last.index, df_last['Close'], label='Close')
    plt.plot(df_last.index, df_last['SMA7'], label='SMA 7')
    plt.plot(df_last.index, df_last['SMA30'], label='SMA 30')
    plt.title('Tesla Stock Price - Last 6 Months')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig('site_src/assets/price_sma.png', dpi=150)


if __name__ == '__main__':
    main()
