"""TODO: This file will connect with sources for data, and get the datasets"""

import pandas as pd
import requests
import json
import csv
import plotly.figure_factory as ff
import sys
from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QListView,
    QLabel,
    QAbstractItemView,
    QMessageBox,
    QLineEdit,
    QAction,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QTableView, QDialog, qApp, QGroupBox, QFormLayout, QComboBox, QDialogButtonBox)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem)
class fundLookup(QWidget):
    def __init__(self, etfs):
        super(fundLookup, self).__init__()
        self.title = "Fund"
        self.left = 600        
        self.top = 400     
        self.width = 400        
        self.height = 125
        self.initUI()
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        header = QLabel()
        header.setText("Fund Input")
        input_etf_label = QLabel()
        input_etf_label.setText("Choose an ETF:")
        self.input_etf_box = QComboBox()
        etf_list = list(etfs.keys())
        etf_list.sort()
        for i in etf_list:
            self.input_etf_box.addItem(i)
        input_stock_label = QLabel()
        input_stock_label.setText("Input your stock ticker (EX: 'AAPL'):")
        self.input_stock_line = QLineEdit(self)
        self.search_button = QPushButton("Search", self)
        self.search_button.setEnabled(False)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setEnabled(True)
        input_etf_layout = QHBoxLayout()
        input_etf_layout.addWidget(input_etf_label)
        input_etf_layout.addWidget(self.input_etf_box)
        input_stock_layout = QHBoxLayout()
        input_stock_layout.addWidget(input_stock_label)
        input_stock_layout.addWidget(self.input_stock_line)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.cancel_button)
        vertical = QVBoxLayout()
        vertical.addWidget(header)
        vertical.addLayout(input_etf_layout)
        vertical.addLayout(input_stock_layout)
        vertical.addLayout(button_layout)
        self.setLayout(vertical)
        self.input_stock_line.textChanged.connect(self.enable_search_button)
        self.cancel_button.clicked.connect(self.cancel)
        self.search_button.clicked.connect(self.search)
    def enable_search_button(self):
        if len(self.input_stock_line.text()) > 0:
            self.search_button.setEnabled(True)
        else:
            self.search_button.setEnabled(False)
    def cancel(self):
        exit()
    def search(self):
        global inputted_ticker
        ticker = str(self.input_etf_box.currentText())
        inputted_ticker = str(self.input_stock_line.text())
        if str(self.input_stock_line.text()) not in etfs[ticker]:
            etfs[ticker].append(str(self.input_stock_line.text()).upper())
        self.close()
        runMain(etfs[ticker])

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

#stocks = get_ticker("RETL")
remove_stocks = []

# stocks = ["ZION","XLF","WRB","WLTW","WFC","USB","UNM","TRV","TROW","TFC","SYF","STT","SPGI","SIVB","SCHW","RJF","RF","RE","PRU","PNC","PGR","PFG","PBCT","NTRS","NDAQ","MTB","MSCI","MS","MMC","MKTX","MET","MCO","LNC","L","KEY","JPM","IVZ","ICE","HIG","HBAN","GS","GL","FRC","FITB","ETFC","DFS","COF","CME","CMA","CINF","CFG","CBOE","CB","C","BRK.B","BLK","BK","BEN","BAC","AXP","AON","AMP","ALL","AJG","AIZ","AIG","AFL"]
# stocks = ["KO", "AMZN", "HD", "MCD", "NKE", "SBUX", "LOW", "BKNG", "TJX", "TGT", "GM", "ROST", "DG", "MAR", "F", "ORLY", "YUM", "HLT", "VFC", "AZO", "EBAY", "LVS", "APTV", "CMG", "RCL", "DLTR", "BBY", "CCL", "DHI", "LEN", "MGM", "KMX", "ULTA", "EXPE", "GPC", "GRMN", "TIF", "DRI", "NVR", "HAS", "WYNN", "NCLH", "PHM", "TSCO", "AAP", "LKQ", "WHR", "BWA", "MHK", "TPR", "NWL", "KSS", "PVH", "LEG", "RL", "CPRI", "HOG", "M", "HBI", "HRB", "LB", "JWN", "GPS", "UAA", "UA"]
# stocks = ['VNOM','MPC','BKR','HAL','SLB','XOM','NOV','PSX','HP','CVX','VLO','APA','NBL','KMI','OXY','FTI','WMB','FANG','HFC','MRO','DVN','CXO','OKE','XEC','EOG','COP','COG','PXD']
# stocks = ["GAS", "AET", "EQM", "CQP" , "TCP" , "CEQP" , "WES" , "DCP" , "MPLX" , "EPD" , "ET" , "ENLC" , "ENBL"]
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
        return [0,0,0]
    comp_key_stats = response.json()
    if comp_key_stats == {}:
        return [0,0,0]
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
    try:
        if (type(comp_key_stats["marketcap"]) != float and type(comp_key_stats["marketcap"]) != int):
            comp_stats += [0]
        else:
            comp_stats += [comp_key_stats["marketcap"]]
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
        if (type(comp_adv_stats["priceToSales"]) != float and type(comp_adv_stats["priceToSales"]) != int):
            comp_info["PS Ratio"] = 0
        else:
            comp_info["PS Ratio"] = comp_adv_stats["priceToSales"]
    except:
        comp_info["PS Ratio"] = 0
    try:
        if (type(comp_adv_stats["priceToBook"]) != float and type(comp_adv_stats["priceToBook"]) != int):
            comp_info["PB Ratio"] = 0
        else:
            comp_info["PB Ratio"] = comp_adv_stats["priceToBook"]
    except:
        comp_info["PB Ratio"] = 0
    if comp_adv_stats["EBITDA"] == 0 or comp_adv_stats["enterpriseValue"] == 0 or type(comp_adv_stats["EBITDA"]) != int:
        comp_info["EBITDA to EV"] = 0
        print(ticker)
    else:
        comp_info["EBITDA to EV"] = (comp_adv_stats["EBITDA"]) / (comp_adv_stats["enterpriseValue"])
    print(comp_info)
    return comp_info

def build_company_dict(ticker):
    metrics_dict = get_advanced_stats(ticker)
    print(metrics_dict)
    dy_pe = get_key_stats(ticker)
    dy = dy_pe[0]
    pe_r = dy_pe[1]
    market_cap = dy_pe[2]
    metrics_dict["Dividend Yield"] = dy
    metrics_dict["PE Ratio"] = pe_r
    cash_flow = get_cash_flow(ticker)
    curr_price = get_curr_price(ticker)
    if (type(market_cap) == float or type(market_cap) == int) and (type(cash_flow) == float or type(cash_flow) == int):
        try:
            metrics_dict["Price to Cashflow"] = float(market_cap) / float(cash_flow)
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
def runMain(stocks):
    global inputted_ticker
    df = build_dataset(stocks)
    print("Took {}".format(time.time() - start_time))
    df = df.fillna(0)
    df_copy = df


    print(df.head())
    ps_nonzero_mean = df[ df["PS Ratio"] != 0 ].mean()
    ps_nonzero_std = df[ df["PS Ratio"] != 0 ].std()
    df["PS Ratio"] = df["PS Ratio"].replace(0.0 , ps_nonzero_mean[0])
    pb_nonzero_mean = df[ df["PB Ratio"] != 0 ].mean()
    pb_nonzero_std = df[ df["PB Ratio"] != 0 ].std()
    df["PB Ratio"] = df["PB Ratio"].replace(0.0 , pb_nonzero_mean[1])
    ev_nonzero_mean = df[ df["EBITDA to EV"] != 0 ].mean()
    ev_nonzero_std = df[ df["EBITDA to EV"] != 0 ].std()
    df["EBITDA to EV"] = df["EBITDA to EV"].replace(0.0 , ev_nonzero_mean[2])
    pe_nonzero_mean = df[ df["PE Ratio"] != 0 ].mean()
    pe_nonzero_std = df[ df["PE Ratio"] != 0 ].std()
    df["PE Ratio"] = df["PE Ratio"].replace(0.0 , pe_nonzero_mean[3])
    dy_nonzero_mean = df[ df["Dividend Yield"] != 0 ].mean()
    dy_nonzero_std = df[ df["Dividend Yield"] != 0 ].std()
    df["Dividend Yield"] = df["Dividend Yield"].replace(0.0 , dy_nonzero_mean[4])
    pc_nonzero_mean = df[ df["Price to Cashflow"] != 0 ].mean()
    pc_nonzero_std = df[ df["Price to Cashflow"] != 0 ].std()
    df["Price to Cashflow"] = df["Price to Cashflow"].replace(0.0 , pc_nonzero_mean[5])
    ndc_nonzero_mean = df[ df["Net Debt Change"] != 0 ].mean()
    ndc_nonzero_std = df[ df["Net Debt Change"] != 0 ].std()
    df["Net Debt Change"] = df["Net Debt Change"].replace(0.0 , ndc_nonzero_mean[6])
    print(df.head())
    df.to_csv("ratios.csv")
    import os
    os.system("python rank.py")

    print(df_copy.head())
    hist_data = [df_copy[ (df_copy["PS Ratio"] != 0) & (df_copy["PS Ratio"] < (ps_nonzero_mean[0] + 3*ps_nonzero_std[0])) & (df_copy["PS Ratio"] > (ps_nonzero_mean[0] - 3*ps_nonzero_std[0])) ].iloc[:,0].values.tolist()]
    group_labels = ["PS Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "PS Ratio Fitted Normal Curve", xaxis_title = "PS Ratio", font = dict(size = 22),
    annotations=[
        dict(
            x= df_copy.at[inputted_ticker, 'PS Ratio'],
            y=0,
            xref="x",
            yref="y",
            text= inputted_ticker + " PS",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ])
    fig.show()
    hist_data = [df_copy[ (df_copy["PB Ratio"] != 0) & (df_copy["PB Ratio"] < (pb_nonzero_mean[1] + 3*pb_nonzero_std[1])) & (df_copy["PB Ratio"] > (pb_nonzero_mean[1] - 3*pb_nonzero_std[1])) ].iloc[:,1].values.tolist()]
    group_labels = ["PB Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "PB Ratio Fitted Normal Curve", xaxis_title = "PB Ratio", font = dict(size = 22),
    annotations=[
        dict(
            x= df_copy.at[inputted_ticker, 'PB Ratio'],
            y=0,
            xref="x",
            yref="y",
            text= inputted_ticker + " PB",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
    )
    fig.show()
    hist_data = [df_copy[ (df_copy["EBITDA to EV"] != 0) & (df_copy["EBITDA to EV"] < (ev_nonzero_mean[2] + 3*ev_nonzero_std[2])) & (df_copy["EBITDA to EV"] > (ev_nonzero_mean[2] - 3*ev_nonzero_std[2])) ].iloc[:,2].values.tolist()]
    group_labels = ["EBITDA to EV Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "EBITDA to EV Ratio Fitted Normal Curve", xaxis_title = "EBITDA to EV", font = dict(size = 22), 
    annotations=[
        dict(
            x= df_copy.at[inputted_ticker, 'EBITDA to EV'],
            y=0,
            xref="x",
            yref="y",
            text= inputted_ticker + " EtEV",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
    )
    fig.show()
    hist_data = [df_copy[ (df_copy["PE Ratio"] != 0) & (df_copy["PE Ratio"] < (pe_nonzero_mean[3] + 3*pe_nonzero_std[3])) & (df_copy["PE Ratio"] > (pe_nonzero_mean[3] - 3*pe_nonzero_std[3])) ].iloc[:,3].values.tolist()]
    group_labels = ["PE Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "PE Ratio Fitted Normal Curve", xaxis_title = "PE Ratio", font = dict(size = 22), 
    annotations=[
        dict(
            x= df_copy.at[inputted_ticker, 'PE Ratio'],
            y=0,
            xref="x",
            yref="y",
            text= inputted_ticker + " PE",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
    )
    fig.show()
    hist_data = [df_copy[ (df_copy["Dividend Yield"] != 0) & (df_copy["Dividend Yield"] < (dy_nonzero_mean[4] + 3*dy_nonzero_std[4])) & (df_copy["Dividend Yield"] > (dy_nonzero_mean[4] - 3*dy_nonzero_std[4])) ].iloc[:,4].values.tolist()]
    group_labels = ["Dividend Yield Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "Dividend Yield Fitted Normal Curve", xaxis_title = "Dividend Yield", font = dict(size = 22), 
    annotations=[
        dict(
            x= df_copy.at[inputted_ticker, 'Dividend Yield'],
            y=0,
            xref="x",
            yref="y",
            text= inputted_ticker + " DY",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
    )
    fig.show()
    print(pc_nonzero_mean, pc_nonzero_std)
    print(pc_nonzero_mean[5] + 5*pc_nonzero_std[5])
    hist_data = [df_copy[ (df_copy["Price to Cashflow"] != 0) & (df_copy["Price to Cashflow"] < (pc_nonzero_mean[5] + 3*pc_nonzero_std[5])) & (df_copy["Price to Cashflow"] > (pc_nonzero_mean[5] - 3*pc_nonzero_std[5])) ].iloc[:,5].values.tolist()]
    group_labels = ["Price to Cashflow Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "Price to Cashflow Fitted Normal Curve", xaxis_title = "Price to Cashflow", font = dict(size = 22), 
    annotations=[
        dict(
            x= df_copy.at[inputted_ticker, 'Price to Cashflow'],
            y=0,
            xref="x",
            yref="y",
            text= inputted_ticker + " PtC",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
    )
    fig.show()
    hist_data = [df_copy[ (df_copy["Net Debt Change"] != 0) & (df_copy["Net Debt Change"] < (ndc_nonzero_mean[6] + 3*ndc_nonzero_std[6])) & (df_copy["Net Debt Change"] > (ndc_nonzero_mean[6] - 3*ndc_nonzero_std[6])) ].iloc[:,6].values.tolist()]
    group_labels = ["Net Debt Change Distribution"]
    fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
    fig.update_layout(title = "Net Debt Change Fitted Normal Curve", xaxis_title = "Net Debt Change", font = dict(size = 22), 
    annotations=[
        dict(
            x= df_copy.at[inputted_ticker, 'Net Debt Change'],
            y=0,
            xref="x",
            yref="y",
            text= inputted_ticker + " NDC",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ]
    )
    fig.show()

if __name__== "__main__" :
    import time
    start_time = time.time()
    etfs = read_csv("Direxion-ETFs-Daily-Holdings-File.csv")
    app = QApplication(sys.argv)
    main = fundLookup(etfs)
    main.show()
    exit_code = app.exec_()
    sys.exit(exit_code)
    