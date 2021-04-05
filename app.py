
import numpy as np
import streamlit as st
from bokeh.plotting import figure


st.title("Stock Price 5")

import requests
import json 
key = 'EGFI6S3850S7AASC'
ticker = 'AAPL'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}'.format(ticker, key)

response = requests.get(url)
data = ((response.json()) ) 

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

p = figure(
    title="Stock Price",
    x_axis_label="time",
    y_axis_label="price")

p.line(x, y, line_width=3)

#p.xaxis.fixed_location = 0
#p.yaxis.fixed_location = 0

st.bokeh_chart(p, use_container_width=True)



