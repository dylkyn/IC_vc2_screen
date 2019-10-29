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
    for i in range(len(stocks)):
        alist = df.loc[i].tolist()
        #print(alist)
        if alist[1] == 0:
            pb = 0
        else:
            pb = alist[1]
        if alist[6] == 0:
            pe = 0
        else:
            pe = alist[6]
        if alist[3] == 0:
            ps = 0
        else:
            ps = alist[3]
        if alist[4] == 0:
            e_ev = 0
        else:
            e_ev = 1 / alist[4]
        if alist[5] == 0:
            pcf = 0
        else:
            pcf = alist[8] / alist[5]
        if alist[7] == 0:
            dy = 0
        else:
            dy = alist[7]
        if alist[2] == 0:
            sy = 0
        else:
            sy = (alist[9] - alist[10] + alist[11]) / alist[2]
        if i == 0:
            adict["pb"] = [pb]
            adict["pe"] = [pe]
            adict["ps"] = [ps]
            adict["e_ev"] = [e_ev]
            adict["pcf"] = [pcf]
            adict["dy"] = [dy]
            adict["sy"] = [sy]
        else:
            adict["pb"] += [pb]
            adict["pe"] += [pe]
            adict["ps"] += [ps]
            adict["e_ev"] += [e_ev]
            adict["pcf"] += [pcf]
            adict["dy"] += [dy]
            adict["sy"] += [sy]
calc_ratios()

newdf = pd.DataFrame(adict,index = ["AAPL","MSFT","F","FIT","TWTR","AMZN","ATVI","MMM","CVX","UNP"])
print(newdf)
ratios = newdf.to_csv("ratios.csv")