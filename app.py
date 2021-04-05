meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests"
import streamlit as st
from bokeh.plotting import figure, show

x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

p = figure(
    title='simple line example',
    x_axis_label='x',
    y_axis_label='y')
    
p.line(x, y)

st.bokeh_chart(p, use_container_width=True)


