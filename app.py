#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 11:43:40 2021

@author: michaelrobinson
"""
import pandas as pd
import streamlit as st
from bokeh.plotting import figure, show
import requests
import json 
import altair as alt


df = pd.read_csv('Documents/allow_prob_TC.csv')

st.title("Patent Technology")
#st.text_input("ENTER NO")

            

option_tech = st.sidebar.selectbox("Technology", (df['TC']))             


tech_allow = df.loc[df['TC'] == option_tech, 'Percent Allowance'].values[0]
'You selected: ', option_tech   
'The probability that your patent will be approved with 2 years is:', tech_allow


#st.bar_chart(df[['Percent Allowance', 'TC']]) 

#x = df['TC'].values
#y = df['Percent Allowance'].values


brush = alt.selection(type='interval', encodings=['x'])

bars = alt.Chart(df).mark_bar().encode(
    x='TC',
    y='Percent Allowance',
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
).add_selection(
    brush
)

line = alt.Chart().mark_rule(color='firebrick').encode(
    y='mean(Percent Allowance):Q',
    size = alt.SizeValue(3)
).transform_filter(
    brush
)

c = alt.layer(bars, line, data=df)


st.altair_chart(c, use_container_width=True)
