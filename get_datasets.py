"""TODO: This file will connect with sources for data, and get the datasets"""
import pandas as pd
import requests
import json 

response = requests.get("https://financialmodelingprep.com/api/v3/company-key-metrics/AAPL?period=quarter")

print(response.json())