import pandas as pd
import streamlit as st
from bokeh.plotting import figure, show
import requests
import json 

#x = [1, 2, 3, 4, 5]
#y = [6, 7, 2, 4, 5]

#p = figure(
#     title='simple line example',
#     x_axis_label='x',
#     y_axis_label='y')
    
# p.line(x, y, legend_label='Trend', line_width=2)

#st.bokeh_chart(p, use_container_width=True)

st.title("Stock Price")
st.text("Enter Stock")

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
st.line_chart(prices2)
