from pprint import pprint
import yfinance as yf
import pandas as pd


def main():
    # print('xxx')
    # yfinance sample request
    # t = yf.Ticker("7203.T")
    # pprint(t.info)
    # h = t.history(period="1mo")
    # print(h.head())

    # extract list data
    # private list
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    # get private list
    df = pd.read_excel(
        "./testdata/20250301_investment.xlsx",
        sheet_name="四季報"
    )
    private_stock_infos = df[["code", "会社名"]]
    pprint(private_stock_infos)
    # get jpx list
    df = pd.read_excel(
        "./testdata/data_j.xls",
        sheet_name="Sheet1"
    )
    jpx_stock_infos = df[["コード", "銘柄名"]]
    pprint(jpx_stock_infos)


if __name__ == '__main__':
    main()
