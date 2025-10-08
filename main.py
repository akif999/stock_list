import sys
from pprint import pprint
import yfinance as yf
import pandas as pd

CODE = 'コード'
NAME = '銘柄名'
I_CLASS33 = '33業種区分'
I_CLASS17 = '17業種区分'
S_DISTINCTION = '規模区分'
SUMMARY = '四季報サマリ'
URL = 'URL'


def main():
    # yfinance sample request
    # codes = []
    # with open("./codes.txt", "r", encoding="utf-8") as f:
    #     for line in f:
    #         codes.append(line.strip())
    # for code in codes:
    #     t = yf.Ticker(code+".T")
    #     url = t.info.get("website", "N/A")
    #     print(code + " " + url)
    # t = yf.Ticker("7203.T")
    # pprint(t.info)
    # h = t.history(period="1mo")
    # print(h.head())
    update_stock_list()
    print("done.")


def update_stock_list():
    # extract list data
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df = pd.read_excel(
        "./testdata/20250301_investment.xlsx",
        sheet_name="四季報"
    )
    df_private = df[[CODE, NAME, I_CLASS33,
                     I_CLASS17, S_DISTINCTION, SUMMARY, URL]]
    df = pd.read_excel(
        "./testdata/data_j.xls",
        sheet_name="Sheet1"
    )
    df_jpxs = df[[CODE, NAME, I_CLASS33, I_CLASS17, S_DISTINCTION]]

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
            'code': str(p_row[CODE]).strip(),
            'name': str(p_row[NAME]).strip(),
            'i_class33': str(p_row[I_CLASS33]).strip(),
            'i_class17': str(p_row[I_CLASS17]).strip(),
            's_distinction': str(p_row[S_DISTINCTION]).strip(),
            'summary': str(p_row[SUMMARY]).strip(),
            'url': str(p_row[URL]).strip()
        }

        j_row = jpx_stock_infos[jpx_stock_infos[CODE] == p_row[CODE]]
        print(f"{p_row[CODE]}", end=': ')
        if (not j_row.empty):
            j_row = j_row.iloc[0]
            if j_row[NAME] != p_row[NAME]:
                print(f"{p_row[NAME]} -> {j_row[NAME]}", end='')
                info['name'] = j_row[NAME]
            if j_row[I_CLASS33] != p_row[I_CLASS33]:
                print(f"{p_row[I_CLASS33]} -> {j_row[I_CLASS33]}", end='')
                info['i_class33'] = j_row[I_CLASS33]
            # if not ETF
            if info['i_class33'] != '-':
                if j_row[I_CLASS17] != p_row[I_CLASS17]:
                    print(f"{p_row[I_CLASS17]} -> {j_row[I_CLASS17]}", end='')
                    info['i_class17'] = j_row[I_CLASS17]
                if j_row[S_DISTINCTION] != p_row[S_DISTINCTION]:
                    print(
                        f"{p_row[S_DISTINCTION]} -> {j_row[S_DISTINCTION]}", end='')
                    info['s_distinction'] = j_row[S_DISTINCTION]
                if info['summary'] == 'nan':
                    pass
                if info['url'] == 'nan':
                    print("xxxx", file=sys.stderr)
                    info['url'] = yf.Ticker(
                        info['code']+".T"
                    ).info.get("website", "N/A")
            print()
        else:
            pass
            print(f'{p_row[CODE]} is nothing in jpx')
        merged_info.append(info)

    print()
    print("merged names")
    for info in merged_info:
        print(
            f"{info['code']}\t{info['name']}\t{info['i_class33']}\t{info['i_class17']}\t{info['s_distinction']}\t{info['summary']}\t{info['url']}")


if __name__ == '__main__':
    main()
