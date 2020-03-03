"""TODO: This file will connect with sources for data, and get the datasets"""

import pandas as pd
import requests
import json
import csv
import itertools

with open('tickers.csv', 'r') as file:
    reader = csv.reader(file, dialect='excel')
    stocks = list(itertools.chain.from_iterable(zip(*reader)))
    print(stocks)

#stocks = ["EQM", "CQP" , "TCP" , "CEQP" , "WES" , "DCP" , "MPLX" , "EPD" , "ET" , "ENLC" , "ENBL"]
#stocks = ['AAPL' , 'MSFT', "F", "FIT", "TWTR", "AMZN", "ATVI", "MMM", "CVX", "UNP"]
req_attr = ["PS Ratio",
            "PB Ratio" ,
            "EBITDA to EV",
            "Dividend Yield",
            "PE Ratio",
            "Price to Cashflow",
            "Net Debt Change"
           ]

def get_curr_price(ticker):
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/price?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/price?token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    result = response.json()
    return result

def get_change_in_debt(ticker):
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/balance-sheet?period=annual&last=2&token=Tpk_81818462745e48e7821ce49f070f5816".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_dc = response.json()
    print(ticker)
    tot_debt_current = comp_dc["balancesheet"][0]["totalLiabilities"] if comp_dc["balancesheet"] is not None else None
    tot_debt_last_yr = comp_dc["balancesheet"][1]["totalLiabilities"] if len(comp_dc["balancesheet"]) > 1 else None
    debt_change = (tot_debt_last_yr - tot_debt_current) / tot_debt_current if tot_debt_last_yr is not None and tot_debt_current is not None else None
    return debt_change

def get_cash_flow(ticker):
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/cash-flow?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/cash-flow?token=Tpk_81818462745e48e7821ce49f070f5816".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_cf = response.json()
    cf = comp_cf["cashflow"][0]["cashFlow"] if len(comp_cf["cashflow"]) > 0 else 0
    return cf

def get_key_stats(ticker):
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/balance-sheet?period=annual&last=2&token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/balance-sheet?period=annual&last=2&token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_dc = response.json()
    try:
        tot_debt_current = comp_dc["balancesheet"][0]["totalLiabilities"]
        tot_debt_last_yr = comp_dc["balancesheet"][1]["totalLiabilities"]
        debt_change = (tot_debt_last_yr - tot_debt_current) / tot_debt_current
        return debt_change
    except:
        debt_change = 0
        return debt_change

def get_advanced_stats(ticker):
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/advanced-stats?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/advanced-stats?token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_adv_stats = response.json()
    comp_info =  dict.fromkeys(req_attr, 0)
    comp_info["PS Ratio"] = comp_adv_stats["priceToSales"]
    comp_info["PB Ratio"] = comp_adv_stats["priceToBook"]
    if comp_adv_stats["EBITDA"] == 0 or comp_adv_stats["enterpriseValue"] == 0 or type(comp_adv_stats["EBITDA"]) != int:
        comp_info["EBITDA to EV"] = 0
        print(ticker)
    else:
        comp_info["EBITDA to EV"] = (comp_adv_stats["EBITDA"]) / (comp_adv_stats["enterpriseValue"])
    return comp_info

def build_company_dict(ticker):
    metrics_dict = get_advanced_stats(ticker)
    dy_pe = get_key_stats(ticker)
    dy = dy_pe[0]
    pe_r = dy_pe[1]
    metrics_dict["Dividend Yield"] = dy
    metrics_dict["PE Ratio"] = pe_r
    cash_flow = get_cash_flow(ticker)
    curr_price = get_curr_price(ticker)
    if (type(curr_price) == float or type(curr_price) == int) and (type(cash_flow) == float or type(cash_flow) == int):
        try:
            metrics_dict["Price to Cashflow"] = float(curr_price) / float(cash_flow)
        except:
            metrics_dict["Price to Cashflow"] = 0
    else:
        metrics_dict["Price to Cashflow"] = 0
    metrics_dict["Net Debt Change"] = get_change_in_debt(ticker)
    return metrics_dict

def build_dataset(stocks):
    # company_metrics_dict = build_company_dict(stocks[0])
    df = pd.DataFrame(index=stocks, columns=["PS Ratio","PB Ratio","EBITDA to EV","PE Ratio","Dividend Yield","Price to Cashflow","Net Debt Change"])
    for ticker in stocks:
        df.loc[ticker] = build_company_dict(ticker)
    return df

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

def rank_ticker():
    #TODO: handle 0s, rank starting from 1
    rank_ratio()
    df["ratios_total"] = df.loc[:, "pb_rank":"dc_rank"].sum(axis=1)
    df['VC2 Score'] = df['ratios_total'].rank(pct=True, ascending=True) * 100
    result_df = df.loc[:, "PB Ratio":"Net Debt Change"]
    result_df["VC2_Score"] = df["VC2 Score"]
    result_df.sort_values(by = "VC2_Score", axis=0, ascending=True, inplace=True, kind='quicksort', na_position='last')
    return result_df

if __name__== "__main__" :
    import time
    start_time = time.time()
    df = build_dataset(stocks)
    print("Took {}".format(time.time() - start_time))
    print(df.head())
    # nonzero_mean = 0
    # nonzero_mean = df[ df["PS Ratio"] != 0 ].mean()
    # df.loc[ df["PS Ratio"] == 0, "PS Ratio" ] = nonzero_mean
    # nonzero_mean = df[ df["PB Ratio"] != 0 ].mean()
    # df.loc[ df["PB Ratio"] == 0, "PB Ratio" ] = nonzero_mean
    # nonzero_mean = df[ df["EBITDA to EV"] != 0 ].mean()
    # df.loc[ df["EBITDA to EV"] == 0, "EBITDA to EV"] = nonzero_mean
    # nonzero_mean = df[ df["PE Ratio"] != 0 ].mean()
    # df.loc[ df["PE Ratio"] == 0, "PE Ratio"] = nonzero_mean
    # nonzero_mean = df[ df["Dividend Yield"] != 0 ].mean()
    # df.loc[ df["Dividend Yield"] == 0, "Dividend Yield"] = nonzero_mean
    # nonzero_mean = df[ df["Price to Cashflow"] != 0 ].mean()
    # df.loc[ df["Price to Cashflow"] == 0, "Price to Cashflow"] = nonzero_mean
    # nonzero_mean = df[ df["Net Debt Change"] != 0 ].mean()
    # df.loc[ df["Net Debt Change"] == 0, "Net Debt Change"] = nonzero_mean
    df.to_csv("ratios.csv")

# import rank
