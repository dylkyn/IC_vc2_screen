"""TODO: This file will connect with sources for data, and get the datasets"""

import pandas as pd
import requests
import json
import csv
import plotly.figure_factory as ff

def read_csv(csv_name):
	with open(csv_name, "r", encoding = "utf8") as etf_file:
		reader = csv.reader(etf_file)
		reader = list(reader)
		etf_dict = {}
		for i in range(1, len(reader)):
			if reader[i][1] not in etf_dict.keys() and len(reader[i][2]) > 0:
				etf_dict[reader[i][1]] = [reader[i][2]]
			elif reader[i][1] in etf_dict.keys() and len(reader[i][2]) > 0:
				etf_dict[reader[i][1]].append(reader[i][2])
		etf_file.close()
	return etf_dict


def get_ticker(etf_ticker):
	etfs = read_csv("Direxion-ETFs-Daily-Holdings-File.csv")
	if etf_ticker in etfs.keys():
		return etfs[etf_ticker]
	return []
stocks = get_ticker("VSPY")
remove_stocks = []

# stocks = ["ZION","XLF","WRB","WLTW","WFC","USB","UNM","TRV","TROW","TFC","SYF","STT","SPGI","SIVB","SCHW","RJF","RF","RE","PRU","PNC","PGR","PFG","PBCT","NTRS","NDAQ","MTB","MSCI","MS","MMC","MKTX","MET","MCO","LNC","L","KEY","JPM","IVZ","ICE","HIG","HBAN","GS","GL","FRC","FITB","ETFC","DFS","COF","CME","CMA","CINF","CFG","CBOE","CB","C","BRK.B","BLK","BK","BEN","BAC","AXP","AON","AMP","ALL","AJG","AIZ","AIG","AFL"]
# stocks = ["KO", "AMZN", "HD", "MCD", "NKE", "SBUX", "LOW", "BKNG", "TJX", "TGT", "GM", "ROST", "DG", "MAR", "F", "ORLY", "YUM", "HLT", "VFC", "AZO", "EBAY", "LVS", "APTV", "CMG", "RCL", "DLTR", "BBY", "CCL", "DHI", "LEN", "MGM", "KMX", "ULTA", "EXPE", "GPC", "GRMN", "TIF", "DRI", "NVR", "HAS", "WYNN", "NCLH", "PHM", "TSCO", "AAP", "LKQ", "WHR", "BWA", "MHK", "TPR", "NWL", "KSS", "PVH", "LEG", "RL", "CPRI", "HOG", "M", "HBI", "HRB", "LB", "JWN", "GPS", "UAA", "UA"]
# stocks = ['VNOM','MPC','BKR','HAL','SLB','XOM','NOV','PSX','HP','CVX','VLO','APA','NBL','KMI','OXY','FTI','WMB','FANG','HFC','MRO','DVN','CXO','OKE','XEC','EOG','COP','COG','PXD']
# stocks = ["GAS", "AET", "EQM", "CQP" , "TCP" , "CEQP" , "WES" , "DCP" , "MPLX" , "EPD" , "ET" , "ENLC" , "ENBL"]
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
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/price?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/price?token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
    if response.status_code == 404 or response.status_code == 403:
        return 0
    result = response.json()
    return result

def get_change_in_debt(ticker):
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/balance-sheet?period=annual&last=2&token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/balance-sheet?period=annual&last=2&token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
    if response.status_code == 404 or response.status_code == 403:
        return 0
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
    if response.status_code == 404 or response.status_code == 403:
        return 0
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
    global remove_stocks
    if response.status_code == 404 or response.status_code == 403:
        print("the 404 error message is working")
        if ticker not in remove_stocks:
            remove_stocks += [ticker]
        return [0,0]
    comp_key_stats = response.json()
    if comp_key_stats == {}:
        return [0,0]
    comp_stats = []
    try:
        if (type(comp_key_stats["dividendYield"]) != float and type(comp_key_stats["dividendYield"]) != int):
            comp_stats += [0]
        else:
            comp_stats += [comp_key_stats["dividendYield"]]
    except:
        comp_stats += [0]
    try:
        if (type(comp_key_stats["peRatio"]) != float and type(comp_key_stats["peRatio"]) != int):
            comp_stats += [0]
        else:
            comp_stats += [comp_key_stats["peRatio"]]
    except:
        comp_stats += [0]
    return comp_stats

def get_advanced_stats(ticker):
    # response = requests.get("https://cloud.iexapis.com/stable/stock/{}/advanced-stats?token=pk_06dd0bea7ba7428a96270972f47bdf23".format(ticker.upper()))
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/advanced-stats?token=Tsk_17d26919e34d483c9ad0d3d6bdc16882".format(ticker.upper()))
    global remove_stocks
    if response.status_code == 404 or response.status_code == 403:
        print("the 403/ 404 code is working. this is the one inf adv.stats")
        remove_stocks += [ticker]
        return dict.fromkeys(req_attr, 0)
    comp_adv_stats = response.json()
    if comp_adv_stats == {}:
        return dict.fromkeys(req_attr, 0)
    comp_info = dict.fromkeys(req_attr, 0)
    try:
        comp_info["PS Ratio"] = comp_adv_stats["priceToSales"]
    except:
        comp_info["PS Ratio"] = 0
    try:
        comp_info["PB Ratio"] = comp_adv_stats["priceToBook"]
    except:
        comp_info["PB Ratio"] = 0
    if comp_adv_stats["EBITDA"] == 0 or comp_adv_stats["enterpriseValue"] == 0 or type(comp_adv_stats["EBITDA"]) != int:
        comp_info["EBITDA to EV"] = 0
        print(ticker)
    else:
        comp_info["EBITDA to EV"] = (comp_adv_stats["EBITDA"]) / (comp_adv_stats["enterpriseValue"])
    return comp_info

def build_company_dict(ticker):
    metrics_dict = get_advanced_stats(ticker)
    print(metrics_dict)
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
    df = pd.DataFrame(index=stocks, columns=["PS Ratio","PB Ratio","EBITDA to EV","PE Ratio","Dividend Yield","Price to Cashflow","Net Debt Change"])
    for ticker in stocks:
        print(ticker)
        df.loc[ticker] = build_company_dict(ticker)
    print(remove_stocks)
    if len(remove_stocks) > 0:
        for let in remove_stocks:
            df = df.drop(let)
    return df

if __name__== "__main__" :
    import time
    start_time = time.time()
    df = build_dataset(stocks)
    print("Took {}".format(time.time() - start_time))
    df = df.fillna(0)
    hist_data = [df[ df["PS Ratio"] != 0].iloc[:,0].values.tolist()]
    group_labels = ["PS Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "PS Ratio Fitted Normal Curve", xaxis_title = "PS Ratio", font = dict(size = 22))
    fig.show()
    hist_data = [df[ df["PB Ratio"] != 0].iloc[:,1].values.tolist()]
    group_labels = ["PB Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "PB Ratio Fitted Normal Curve", xaxis_title = "PB Ratio", font = dict(size = 22))
    fig.show()
    hist_data = [df[ df["EBITDA to EV"] != 0].iloc[:,2].values.tolist()]
    group_labels = ["EBITDA to EV Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "EBITDA to EV Ratio Fitted Normal Curve", xaxis_title = "EBITDA to EV", font = dict(size = 22))
    fig.show()
    hist_data = [df[ df["PE Ratio"] != 0].iloc[:,3].values.tolist()]
    group_labels = ["PE Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "PE Ratio Fitted Normal Curve", xaxis_title = "PE Ratio", font = dict(size = 22))
    fig.show()
    hist_data = [df[ df["Dividend Yield"] != 0].iloc[:,4].values.tolist()]
    group_labels = ["Dividend Yield Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "Dividend Yield Fitted Normal Curve", xaxis_title = "Dividend Yield", font = dict(size = 22))
    fig.show()
    hist_data = [df[ df["Price to Cashflow"] != 0].iloc[:,5].values.tolist()]
    group_labels = ["Price to Cashflow Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "Price to Cashflow Fitted Normal Curve", xaxis_title = "Price to Cashflow", font = dict(size = 22))
    fig.show()
    hist_data = [df[ df["Net Debt Change"] != 0].iloc[:,6].values.tolist()]
    group_labels = ["Net Debt Change Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "Net Debt Change Fitted Normal Curve", xaxis_title = "Net Debt Change", font = dict(size = 22))
    fig.show()

    print(df.head())
    nonzero_mean = df[ df["PS Ratio"] != 0 ].mean()
    df["PS Ratio"] = df["PS Ratio"].replace(0.0 , nonzero_mean[0])
    nonzero_mean = df[ df["PB Ratio"] != 0 ].mean()
    df["PB Ratio"] = df["PB Ratio"].replace(0.0 , nonzero_mean[1])
    nonzero_mean = df[ df["EBITDA to EV"] != 0 ].mean()
    df["EBITDA to EV"] = df["EBITDA to EV"].replace(0.0 , nonzero_mean[2])
    nonzero_mean = df[ df["PE Ratio"] != 0 ].mean()
    df["PE Ratio"] = df["PE Ratio"].replace(0.0 , nonzero_mean[3])
    nonzero_mean = df[ df["Dividend Yield"] != 0 ].mean()
    df["Dividend Yield"] = df["Dividend Yield"].replace(0.0 , nonzero_mean[4])
    nonzero_mean = df[ df["Price to Cashflow"] != 0 ].mean()
    df["Price to Cashflow"] = df["Price to Cashflow"].replace(0.0 , nonzero_mean[5])
    nonzero_mean = df[ df["Net Debt Change"] != 0 ].mean()
    df["Net Debt Change"] = df["Net Debt Change"].replace(0.0 , nonzero_mean[6])
    print(df.head())
    df.to_csv("ratios.csv")
    import os
    os.system("python rank.py")