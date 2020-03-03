from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
import csv

df = pd.read_csv("ratios.csv", index_col=0)
PS = df["PS Ratio"].hist(bins = 50)
PS.set_title("PS Ratio Histogram")
# PS.set_xlabel("")
plt.show()
style.use("ggplot")
