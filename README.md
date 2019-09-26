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
```get_datasets.py``` ->  ```calc_ratios.py``` -> ```rank.py``` -> ```output.py```

### Input and Output
* Will take in an excel sheet of stock tickers
* Will output excel sheet with VC2 score for every stock in the input csv

### How to Use get_datasets.py 
* ```get_datasets.py``` creates a ```.csv``` file called ```company_metrics.csv```
* To **request data of different stocks**, edit the beginning of the file and add / change the list of stocks (make sure you are using the stock ticker)
* To **run** ```get_datasets.py```, navigate into the ```vc2_screen``` project folder (which has all the proj files, you can check with ```ls```). Run the file with ```python get_datasets.py```
* It will take about 30 sec to run, and after you should see a file in the ```vc2_screen``` folder called ```company_metrics.csv```. The csv contains all the data needed for each company for each of the next parts of the project

### How to use the dataset (.csv) in other files
* Make sure you have pandas installed
* After running ```get_datasets.py```, you can easily access the dataset (company_metrics.csv) in your file by using pandas
* Run  ```df = df.read_csv("company_metrics.csv")``` to load the csv as a pandas dataframe in your folder
* You can now print what the data frame looks like with ```print(df.head())```
* ```df.loc["aapl"].tolist()``` will give you all the stats for aapl in a normal python list, you can replace aapl with any ticker

