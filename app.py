import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from bokeh.plotting import figure


st.title("Stock Price AAPL")

import requests
import json 
key = 'EGFI6S3850S7AASC'
ticker = 'AAPL'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)

response = requests.get(url)
data = ((response.json()) ) 



stock = data['Time Series (Daily)']
df = pd.DataFrame(stock)

date = df.iloc[0,0]
prices1 = df.iloc[4]
prices2 = pd.to_numeric(prices1)

plt.subplot(121)
plt.plot(prices2)


plt.ylabel('Price')
plt.xlabel('Date')
plt.title('Stock')



