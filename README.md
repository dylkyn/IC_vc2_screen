# VC2_Screen

### Goal
* Provide a strategy / screen that quickly determines whether a company is undervalued / overvalued.

### Strategy
1. Calculate following ratios for each stock:
    * Price to Book Value
    * Price to Sales 
    * EBITDA to EV
    * Price to Cashflow 
    * Price to Earnings
    * Shareholder Yield
2. Give each stock a percentile rank 1 - 100 for each of the ratios. Example: if AAPL has the best price to sales out of all the stocks you are looking at, it would get a 1 for Price to Sales bc it is in the top 1% for P / S. If a ratio can't be calculate (like negative P / E) give it a neutral score of 50
3. Add up all the ratio scores for each stock
4. Give the stocks a percentile rank based on the combined scores
5. Each stock will have a number 1 - 100. 1 is the most undervalued out of your universe of stocks, while 100 is the most overvalued

### Flow
```get_datasets.py``` -> ```clean_data.py``` -> ```calc_ratios.py``` -> ```rank.py``` -> ```output.py```

### Input and Output
* Will take in an excel sheet of stock tickers
* Will output excel sheet with VC2 score for every stock in the input csv

