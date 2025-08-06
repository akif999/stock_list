from pprint import pprint
# import yfinance as yf
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
    df_private = df[["code", "会社名"]]
    # print('df_private')
    # pprint(df_private)
    # get jpx list
    df = pd.read_excel(
        "./testdata/data_j.xls",
        sheet_name="Sheet1"
    )
    df_jpxs = df[["コード", "銘柄名"]]
    # print('df_jpxs')
    # pprint(df_jpxs)

    # diff codes
    private_stock_infos = df_private[['code', '会社名']].copy()
    private_stock_infos['code'] = private_stock_infos['code'].astype(
        str).str.strip().str.zfill(4)
    jpx_stock_infos = df_jpxs[['コード', '銘柄名']].copy()
    jpx_stock_infos['コード'] = jpx_stock_infos['コード'].astype(
        str).str.strip().str.zfill(4)
    diff = jpx_stock_infos[~jpx_stock_infos['コード'].isin(
        private_stock_infos['code']
    )]
    print('diff codes')
    pprint(diff)
    print()

    # merge names
    print('merge names followig will be changed')
    pprint(jpx_stock_infos)
    merged_info = []
    for i, p_row in private_stock_infos.iterrows():
        info = {'code': p_row['code'], 'name': p_row['会社名']}
        j_row = jpx_stock_infos[jpx_stock_infos['コード'] == p_row['code']]
        if (not j_row.empty):
            if j_row.iloc[0]['銘柄名'] != p_row['会社名']:
                print(f"{p_row['code']}", end=': ')
                print(f"{p_row['会社名']} -> {j_row.iloc[0]['銘柄名']}")
                info['name'] = j_row.iloc[0]['銘柄名']
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

    # not_matched = jpx_stock_infos[~jpx_stock_infos['コード'].isin(
    #     private_stock_infos['code']
    # )]['コード']
    # pprint(not_matched.tolist())

    # print(private_stock_infos.index)
    # print(jpx_stock_infos.index)


if __name__ == '__main__':
    main()
