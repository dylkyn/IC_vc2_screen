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
    metrics_dict["Market Price"] = curr_price
    return metrics_dict

def build_dataset(stocks):
    company_metrics_dict = build_company_dict('aapl')
    df = pd.DataFrame(index=stocks, columns=['PB ratio', 'Market Cap', 'Revenue per Share', 'Enterprise Value over EBITDA', 'Operating Cash Flow per Share', 'PE ratio', 'Dividend Yield', 'Market Price'])
    for ticker in stocks:
        df.loc[ticker] = build_company_dict(ticker)
    return df

if __name__== "__main__" :
    import time
    start_time = time.time()
    df = build_dataset(stocks)
    print("Took {}".format(time.time() - start_time))
    df.to_csv("company_metrics.csv")