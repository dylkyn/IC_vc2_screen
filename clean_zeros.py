nonzero_mean = 0
for col in ["PS Ratio","PB Ratio","EBITDA to EV","PE Ratio","Dividend Yield","Price to Cashflow","Net Debt Change"]:
    nonzero_mean = df[ df.col != 0 ].mean()
    df.loc[ df.col == 0, "col" ] = nonzero_mean