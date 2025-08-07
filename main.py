from pprint import pprint
# import yfinance as yf
import pandas as pd

CODE = 'コード'
NAME = '銘柄名'
I_CLASS33 = '33業種区分'
I_CLASS17 = '17業種区分'
S_DISTINCTION = '規模区分'


def main():
    # yfinance sample request
    # t = yf.Ticker("7203.T")
    # pprint(t.info)
    # h = t.history(period="1mo")
    # print(h.head())

    # extract list data
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df = pd.read_excel(
        "./testdata/20250301_investment.xlsx",
        sheet_name="四季報"
    )
    df_private = df[[CODE, NAME]]
    df = pd.read_excel(
        "./testdata/data_j.xls",
        sheet_name="Sheet1"
    )
    df_jpxs = df[[CODE, NAME]]

    # diff codes
    private_stock_infos = df_private.copy()
    private_stock_infos[CODE] = private_stock_infos[CODE].astype(
        str).str.strip().str.zfill(4)
    jpx_stock_infos = df_jpxs.copy()
    jpx_stock_infos[CODE] = jpx_stock_infos[CODE].astype(
        str).str.strip().str.zfill(4)
    diff = jpx_stock_infos[~jpx_stock_infos[CODE].isin(
        private_stock_infos[CODE]
    )]
    print('diff codes')
    if diff.empty:
        print("nothing is difference")
    else:
        pprint(diff)
    print()

    # merge names
    print('merge names followig will be changed')
    # pprint(jpx_stock_infos)
    merged_info = []
    for i, p_row in private_stock_infos.iterrows():
        info = {
            'code': p_row[CODE],
            'name': p_row[NAME]
        }
        j_row = jpx_stock_infos[jpx_stock_infos[CODE] == p_row[CODE]]
        if (not j_row.empty):
            if j_row.iloc[0][NAME] != p_row[NAME]:
                print(f"{p_row[CODE]}", end=': ')
                print(f"{p_row[NAME]} -> {j_row.iloc[0][NAME]}")
                info['name'] = j_row.iloc[0][NAME]
            else:
                pass
                # print('names are same')
        else:
            pass
            # print('code is nothing in jpx')
        merged_info.append(info)

    print()
    print("merged names")
    for info in merged_info:
        print(f"{info['code']}\t{info['name']}")


if __name__ == '__main__':
    main()
