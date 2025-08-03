import yfinance as yf


def main():
    print('xxx')
    # yfinance sample request
    t = yf.Ticker("7203.T")
    df = t.history(period="1mo")
    print(df.head())


if __name__ == '__main__':
    main()
