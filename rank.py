"""TODO: Take the ratios from calc_ratios.py, and do the 2 rounds of ranking for each stock
Assume you have all the necessary inputs from the previous file, like the ratio values for each company
"""
import pandas as pd
import numpy as np

df = pd.read_csv("ratios.csv")

def rank_ratio():
    df['PB ratio rank'] = df['Pb ratio'].rank(ascending=False)
    df['PS ratio rank'] = df['PS ratio'].rank(ascending=False)
    df['EBITDA to EV ratio rank'] = df['EBITDA to EV ratio'].rank(ascending=False)
    df['PCF ratio rank'] = df['PCF ratio'].rank(ascending=False)
    df['PE ratio rank'] = df['PE ratio'].rank(ascending=False)
    df['shareholder yield rank'] = df['shareholder yield'].rank(ascending=False)

def rank_ticker():
    rank_ratio()
    df['ratio_avg'] = df.loc[:, 'PB ratio rank':'sharehold yield rank'].mean(axis=0, numeric_only=True)
    df['ratio_rank'] = df['ratio_avg'].rank(ascending=False)

if __name__ == '__main__':
    rank_ratio()
    rank_ticker()
    df.to_csv("vc2output.csv")
