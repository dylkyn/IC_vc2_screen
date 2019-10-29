"""TODO: This file will connect with sources for data, and get the datasets"""

import pandas as pd
import requests
import json 

stocks = ['AAPL' , 'MSFT', "F", "FIT", "TWTR", "AMZN", "ATVI", "MMM", "CVX", "UNP"]
req_attr = ["PB ratio" , 
            "Market Cap",
            "Revenue per Share", 
            "Enterprise Value over EBITDA",
            "Operating Cash Flow per Share",
            "PE ratio",
            "Dividend Yield",
           ]
def get_curr_price(ticker):
    response = requests.get("https://financialmodelingprep.com/api/v3/historical-price-full/{}?serietype=line".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    result = response.json()
    return result["historical"][-1]["close"]    

def get_reported_financials(ticker):
    response = requests.get("https://sandbox.iexapis.com/stable/time-series/REPORTED_FINANCIALS/{}/10-Q?token=Tpk_07d1028083ce4edc98dc3d09d76092d7".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_key_stats = response.json()
    stock_transaction_list = []
    if "StockRepurchasedAndRetiredDuringPeriodValue" in comp_key_stats[0].keys():
        stock_transaction_list += [comp_key_stats[0]["StockRepurchasedAndRetiredDuringPeriodValue"]]
    else:
        stock_transaction_list += [0]
    if "StockIssuedDuringPeriodValueNewIssues" in comp_key_stats[0].keys():
        stock_transaction_list += [comp_key_stats[0]["StockIssuedDuringPeriodValueNewIssues"]]
    else:
        stock_transaction_list += [0]
    return stock_transaction_list

def get_dividends_paid(ticker):
    response = requests.get("https://sandbox.iexapis.com/stable/stock/{}/cash-flow?token=Tpk_07d1028083ce4edc98dc3d09d76092d7".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    result_dividends_paid = response.json()
    dividends_paid = 0
    if "dividendsPaid" in result_dividends_paid["cashflow"][0].keys() and result_dividends_paid["cashflow"][0]["dividendsPaid"] != "null":
        dividends_paid = result_dividends_paid["cashflow"][0]["dividendsPaid"]
    else:
        dividends_paid = 0
    return dividends_paid

def get_metrics(ticker):
    response = requests.get("https://financialmodelingprep.com/api/v3/company-key-metrics/{}?period=quarter".format(ticker.upper()))
    if response.status_code == 404:
        return "Stock Info not Available"
    comp_key_metrics = response.json()
    values_list = comp_key_metrics["metrics"][0]
    comp_info =  dict.fromkeys(req_attr, 0)
    for attr in req_attr:
        comp_info[attr] = values_list[attr]
    return comp_info

def build_company_dict(ticker):
    metrics_dict = get_metrics(ticker)
    curr_price = get_curr_price(ticker)
    stock_trans_list = get_reported_financials(ticker)
    divi_paid = get_dividends_paid(ticker)
    metrics_dict["Market Price"] = curr_price
    metrics_dict["StockRepurchasedAndRetiredDuringPeriodValue"] = stock_trans_list[0]
    metrics_dict["StockIssuedDuringPeriodValueNewIssues"] = stock_trans_list[1]
    metrics_dict["dividendsPaid"] = divi_paid
    return metrics_dict

def build_dataset(stocks):
    company_metrics_dict = build_company_dict("aapl")
    df = pd.DataFrame(index=stocks, columns=['PB ratio', 'Market Cap', 'Revenue per Share', 'Enterprise Value over EBITDA', 'Operating Cash Flow per Share', 'PE ratio', 'Dividend Yield', 'Market Price',"StockRepurchasedAndRetiredDuringPeriodValue","StockIssuedDuringPeriodValueNewIssues","dividendsPaid"])
    for ticker in stocks:
        df.loc[ticker] = build_company_dict(ticker)
    return df

if __name__== "__main__" :
    import time
    start_time = time.time()
    df = build_dataset(stocks)
    print("Took {}".format(time.time() - start_time))
    print(df.head())
    df.to_csv("company_metrics.csv")
