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

stocks = ["HPQ","CTSH","ADSK","LRCX","ADI","AMD","NOW","AMAT","MU","INTU","QCOM","ORCL","IBM","TXN","AVGO","NVDA","CRM","ADBE","CSCO","INTC","FB","GOOG","GOOGL","MSFT","AAPL","VZ","PYPL","ACN","MA"]
# stocks = ["ILMN","BIIB","VRTX","AGN","BSX","ZTS","SYK","ISRG","BDX","ANTM","CI","GILD","CVS","DHR","LLY","TMO","ABBV","AMGN","BMY","MDT","ABT","PFE","MRK","UNH","JNJ"]
# stocks = ["ZION","XLF","WRB","WLTW","WFC","USB","UNM","TRV","TROW","TFC","SYF","STT","SPGI","SIVB","SCHW","RJF","RF","RE","PRU","PNC","PGR","PFG","PBCT","NTRS","NDAQ","MTB","MSCI","MS","MMC","MKTX","MET","MCO","LNC","L","KEY","JPM","IVZ","ICE","HIG","HBAN","GS","GL","FRC","FITB","ETFC","DFS","COF","CME","CMA","CINF","CFG","CBOE","CB","C","BRK.B","BLK","BK","BEN","BAC","AXP","AON","AMP","ALL","AJG","AIZ","AIG","AFL"]
# stocks = ["XOM","XEC","WMB","VLO","SLB","PXD","PSX","OXY","OKE","NOV","NBL","MRO","MPC","KMI","HP","HFC","HES","HAL","FTI","FANG","EOG","DVN","CXO","CVX","COP","COG","BKR","APA"]
# stocks = ["K", "CHD", "CLX", "KHC", "MKC", "KR", "HSY", "MNST", "ADM", "TSN", "STZ", "GIS", "SYY", "EL", "WBA", "KMB", "CL", "MDLZ", "COST", "PM", "MO", "WMT", "PEP", "KO", "PG"]
# stocks = ["AMZN", "HD", "MCD", "NKE", "SBUX", "LOW", "BKNG", "TJX", "TGT", "GM", "ROST", "DG", "MAR", "F", "ORLY", "YUM", "HLT", "VFC", "AZO", "EBAY", "LVS", "APTV", "CMG", "RCL", "DLTR", "BBY", "CCL", "DHI", "LEN", "MGM", "KMX", "ULTA", "EXPE", "GPC", "GRMN", "TIF", "DRI", "NVR", "HAS", "WYNN", "NCLH", "PHM", "TSCO", "AAP", "LKQ", "WHR", "BWA", "MHK", "TPR", "NWL", "KSS", "PVH", "LEG", "RL", "CPRI", "HOG", "M", "HBI", "HRB", "LB", "JWN", "GPS", "UAA", "UA"]
req_attr = ["PS ratio",
            "PB ratio" ,
            "EBITDA to EV",
            "Dividend Yield",
            "PE ratio",
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

def get_cash_flow(ticker):
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/cash-flow?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/cash-flow?token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
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
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/stats?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/stats?token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_key_stats = response.json()
    comp_stats = []
    comp_stats += [comp_key_stats["dividendYield"]]
    comp_stats += [comp_key_stats["peRatio"]]
    return comp_stats

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
