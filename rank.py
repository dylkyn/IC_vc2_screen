"""TODO: Take the ratios from calc_ratios.py, and do the 2 rounds of ranking for each stock
Assume you have all the necessary inputs from the previous file, like the ratio values for each company
"""
import pandas as pd
import numpy as np

df = pd.read_csv("ratios.csv", index_col=0)

"PS Ratio","PB Ratio","EBITDA to EV","PE Ratio","Dividend Yield","Price to Cashflow","Net Debt Change"

def rank_ratio():
    df['pb_rank'] = df['PB Ratio'].rank(pct=True, ascending=True) * 100
    df['pe_rank'] = df['PE Ratio'].rank(pct=True, ascending=True) * 100
    df['ps_rank'] = df['PS Ratio'].rank(pct=True, ascending=True) * 100
    df['e_ev_rank'] = df['EBITDA to EV'].rank(pct=True, ascending=True) * 100
    df['pcf_rank'] = df['Price to Cashflow'].rank(pct=True, ascending=True) * 100
    df['dy_rank'] = df['Dividend Yield'].rank(pct=True, ascending=False) * 100
    df['dc_rank'] = df['Net Debt Change'].rank(pct=True, ascending=False) * 100

"""def rank_ticker():
    rank_ratio()
    df['ratio_avg'] = df.loc[:, 'pb_rank':'dy_rank'].mean(axis=1, numeric_only=True)
    df['ratio_rank'] = df['ratio_avg'].rank(ascending=False)"""

def rank_ticker(df):
    #TODO: handle 0s, rank starting from 1
    rank_ratio()
    df["ratios_total"] = df.loc[:, "pb_rank":"dc_rank"].sum(axis=1)
    df['VC2 Score'] = df['ratios_total'].rank(pct=True, ascending=True) * 100
    result_df = df.loc[:, "PB Ratio":"Net Debt Change"]
    result_df["VC2_Score"] = df["VC2 Score"]
    result_df.sort_values(by = "VC2_Score", axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
    return result_df

if __name__ == '__main__':
    rank_ratio()
    print(df)
    rank_ticker(df).to_csv("vis_vc2.csv")
