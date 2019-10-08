"""TODO: Take the ratios from calc_ratios.py, and do the 2 rounds of ranking for each stock
Assume you have all the necessary inputs from the previous file, like the ratio values for each company
"""
import pandas as pd
import numpy as np

df = pd.read_csv("ratios.csv", index_col=0)

def rank_ratio():
    df['pb_rank'] = df['pb'].rank(ascending=False)
    df['pe_rank'] = df['pe'].rank(ascending=False)
    df['ps_rank'] = df['ps'].rank(ascending=False)
    df['e_ev_rank'] = df['e_ev'].rank(ascending=False)
    df['pcf_rank'] = df['pcf'].rank(ascending=False)
    df['dy_rank'] = df['dy'].rank(ascending=False)

def rank_ticker():
    rank_ratio()
    df['ratio_avg'] = df.loc[:, 'pb_rank':'dy_rank'].mean(axis=1, numeric_only=True)
    df['ratio_rank'] = df['ratio_avg'].rank(ascending=False)

if __name__ == '__main__':
    rank_ticker()
    print(df)
    df['ratio_rank'].sort_values().to_csv("vc2output.csv")
