"""TODO: This file will connect with sources for data, and get the datasets"""

import pandas as pd
import requests
import json 

import csv
stocks = []
with open('REIT.csv', 'r') as file:
    for row in csv.reader(file):
        stocks.append(row[0])
    file.close()
del stocks[0]

# stocks = ["EQM", "CQP" , "TCP" , "CEQP" , "WES" , "DCP" , "MPLX" , "EPD" , "ET" , "ENLC" , "ENBL"]
#stocks = ['AAPL' , 'MSFT', "F", "FIT", "TWTR", "AMZN", "ATVI", "MMM", "CVX", "UNP"]
req_attr = ["PS ratio",
            "PB ratio" ,
            "EBITDA to EV",
            "Dividend Yield",
            "PE ratio",
            "Price to Cashflow",
            "Net Debt Change"
           ]

def get_curr_price(ticker):
    response = requests.get("https://cloud.iexapis.com/stable/stock/{}/price?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    result = response.json()
    return result

def get_change_in_debt(ticker):
    response = requests.get("https://cloud.iexapis.com/stable/stock/{}/balance-sheet?period=annual&last=2&token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_dc = response.json()
    try:
        tot_debt_current = comp_dc["balancesheet"][0]["totalLiabilities"]
        tot_debt_last_yr = comp_dc["balancesheet"][1]["totalLiabilities"]
        debt_change = (tot_debt_last_yr - tot_debt_current) / tot_debt_current
        return debt_change
    except:
        print(ticker)
        debt_change = 0
        return debt_change

def get_cash_flow(ticker):
    response = requests.get("https://cloud.iexapis.com/stable/stock/{}/cash-flow?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_cf = response.json()
    try:
        cf = comp_cf["cashflow"][0]["cashFlow"]
    except:
        print(ticker)
        cf = 0
        return cf
    return cf

def get_key_stats(ticker):
    response = requests.get("https://cloud.iexapis.com/stable/stock/{}/stats?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_key_stats = response.json()
    comp_stats = []
    comp_stats += [comp_key_stats["dividendYield"]]
    comp_stats += [comp_key_stats["peRatio"]]
    return comp_stats

def get_advanced_stats(ticker):
    response = requests.get("https://cloud.iexapis.com/stable/stock/{}/advanced-stats?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_adv_stats = response.json()
    comp_info =  dict.fromkeys(req_attr, 0)
    comp_info["PS Ratio"] = comp_adv_stats["priceToSales"]
    comp_info["PB Ratio"] = comp_adv_stats["priceToBook"]
    if comp_adv_stats["EBITDA"] == 0 or comp_adv_stats["enterpriseValue"] == 0:
        comp_info["EBITDA to EV"] = 0
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

if __name__== "__main__" :
    import time
    start_time = time.time()
    df = build_dataset(stocks)
    print("Took {}".format(time.time() - start_time))
    print(df.head())
    df.to_csv("ratios.csv")
