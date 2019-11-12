"""TODO: Take the ratios from calc_ratios.py, and do the 2 rounds of ranking for each stock
Assume you have all the necessary inputs from the previous file, like the ratio values for each company
"""
import pandas as pd
import numpy as np

df = pd.read_csv("ratios.csv", index_col=0)

def rank_ratio():
    df['pb_rank'] = df['pb'].rank(pct=True, ascending=True) * 100
    df['pe_rank'] = df['pe'].rank(pct=True, ascending=True) * 100
    df['ps_rank'] = df['ps'].rank(pct=True, ascending=True) * 100
    df['e_ev_rank'] = df['e_ev'].rank(pct=True, ascending=True) * 100
    df['pcf_rank'] = df['pcf'].rank(pct=True, ascending=True) * 100
    df['dy_rank'] = df['dy'].rank(pct=True, ascending=False) * 100

"""def rank_ticker():
    rank_ratio()
    df['ratio_avg'] = df.loc[:, 'pb_rank':'dy_rank'].mean(axis=1, numeric_only=True)
    df['ratio_rank'] = df['ratio_avg'].rank(ascending=False)"""

def rank_ticker(df):
    #TODO: handle 0s, rank starting from 1
    rank_ratio()
    df["ratios_total"] = df.loc[:, "pb_rank":"dy_rank"].sum(axis=1)
    df['VC2 Score'] = df['ratios_total'].rank(pct=True, ascending=True) * 100
    result_df = df.loc[:, "pb":"dy"]
    result_df["VC2_Score"] = df["VC2 Score"]
    result_df.sort_values(by = "VC2_Score", axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
    return result_df

if __name__ == '__main__':
    rank_ratio()
    print(df)
    rank_ticker(df).to_csv("vc2results.csv")
