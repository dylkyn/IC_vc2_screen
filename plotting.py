from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
import csv
import scipy.stats as stats
import pylab as pl
# import plotly.plotly as py
import chart_studio.plotly as py
import plotly.graph_objects as go
import plotly.figure_factory as ff
df = pd.read_csv("ratios.csv", index_col=0)
stock_name = "SCHW"

hist_data = [df[ df["PS Ratio"] != 0].iloc[:,0].values.tolist()]
group_labels = ["PS Distribution"]
fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
fig.update_layout(title = "PS Ratio Fitted Normal Curve", xaxis_title = "PS Ratio", font = dict(size = 22))
fig.show()

hist_data = [df[ df["PB Ratio"] != 0].iloc[:,1].values.tolist()]
print(hist_data)
group_labels = ["PB Distribution"]
fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
fig.update_layout(title = "PB Ratio Fitted Normal Curve", xaxis_title = "PB Ratio", font = dict(size = 22))
fig.show()

hist_data = [df[ df["EBITDA to EV"] != 0].iloc[:,2].values.tolist()]
print(hist_data)
group_labels = ["EBITDA to EV Distribution"]
fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
fig.update_layout(title = "EBITDA to EV Ratio Fitted Normal Curve", xaxis_title = "EBITDA to EV", font = dict(size = 22))
fig.show()

hist_data = [df[ df["PE Ratio"] != 0].iloc[:,3].values.tolist()]
print(hist_data)
group_labels = ["PE Distribution"]
fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
fig.update_layout(title = "PE Ratio Fitted Normal Curve", xaxis_title = "PE Ratio", font = dict(size = 22))
fig.show()

hist_data = [df[ df["Dividend Yield"] != 0].iloc[:,4].values.tolist()]
print(hist_data)
group_labels = ["Dividend Yield Distribution"]
fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
fig.update_layout(title = "Dividend Yield Fitted Normal Curve", xaxis_title = "Dividend Yield", font = dict(size = 22))
fig.show()

hist_data = [df[ df["Price to Cashflow"] != 0].iloc[:,5].values.tolist()]
print(hist_data)
group_labels = ["Price to Cashflow Distribution"]
fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
fig.update_layout(title = "Price to Cashflow Fitted Normal Curve", xaxis_title = "Price to Cashflow", font = dict(size = 22))
fig.show()

hist_data = [df[ df["Net Debt Change"] != 0].iloc[:,6].values.tolist()]
print(hist_data)
group_labels = ["Net Debt Change Distribution"]
fig = ff.create_distplot(hist_data, group_labels, bin_size = "auto", curve_type = "normal", show_hist = True, show_rug = True)
fig.update_layout(title = "Net Debt Change Fitted Normal Curve", xaxis_title = "Net Debt Change", font = dict(size = 22))
fig.show()

# hist_data = [df["PE Ratio"].values.tolist()]
# group_labels = ["PE Distribution"]
# fig = ff.create_distplot(hist_data, group_labels, bin_size = .9, curve_type = "normal", show_hist = True, show_rug = True)
# fig.update_layout(title = "PE Ratio Fitted normal curve", yaxis_title = "Percent", xaxis_title = "PE Ratio", font = dict(size = 22))
# fig.show()
# fit = stats.norm.pdf(df["PS Ratio"], np.mean(df["PS Ratio"]), np.std(df["PS Ratio"]))
# pl.plot(df["PS Ratio"],fit,'-o')
# pl.hist(df["PS Ratio"],density=True, bins = 40)
# pl.annotate("*AAPL's PS Ratio", (1,.1))
# pl.show() 