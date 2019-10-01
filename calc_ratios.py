""" TODO: Take the values from clean_data.py and calc all the ratios for each stock"""
req_attr = ["PB ratio" , 
            "Market Cap",
            "Revenue per Share", 
            "Enterprise Value over EBITDA",
            "Operating Cash Flow per Share",
            "PE ratio",
            "Dividend Yield",
            "Market Price"
           ]
stocks = ['AAPL' , 'MSFT', "F", "FIT", "TWTR", "AMZN", "ATVI", "MMM", "CVX", "UNP"]
import pandas as pd
alist = []
adict = {}
def calc_ratios():
    df = pd.read_csv("company_metrics.csv")
    print(df[:-1])
    for i in range(len(stocks)):
        alist = df.loc[i].tolist()
        #print(alist)
        pb = alist[1]
        pe = alist[6]
        ps = 1 / alist[3]
        if alist[4] == 0:
            e_ev = 0
        else:
            e_ev = 1 / alist[4]
        if alist[5] == 0:
            pcf = 0
        else:
            pcf = alist[8] / alist[5]
        #if
        #dy = alist
        adict[stocks[i]] = [pb,pe,ps,e_ev,pcf]
        alist = []
    #print(adict)
calc_ratios()
def ratio_to_dataframe():
    newdf = pd.DataFrame(adict,index = ["pb","pe","ps","e_ev","pcf"])
    #print(newdf)
ratio_to_dataframe()

#newdf.to_csv("ratios.csv")