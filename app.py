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
import time


df = pd.read_csv('allow_prob_TC.csv')
df_a = pd.read_csv('Allow_prob_1000.csv')

df = df.sort_values(by=['TC'], inplace=False)

df = df.reset_index()
st.title("Will My Patent Be Granted?")


            
st.write("The U.S. Patent and Trademark office publishes datasets including 11 million patent applications. This includes all applications from 1996 to 2018. When each patent application is filed it is assigned to a technology area and classification code. These features were used to create a prediction of the probability of the application being granted. ")


st.write('Select a technology area for your application:')



        
option_tech = st.selectbox("Technology", (df['TC']))             

st.spinner()
with st.spinner(text='Calculating...'):
    time.sleep(2)
    st.success('Done')

df['Percent Allowance f'] = (100. * df['Percent Allowance'])
df['Percent Allowance f'] = (df['Percent Allowance f'].map('{:.0f}%'.format))
tech_allow = df.loc[df['TC'] == option_tech, 'Percent Allowance f'].values[0]


'**You selected:** ',  option_tech 
'**The probability that your patent will be approved with 2 years is:**', tech_allow


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


option_c = st.selectbox("Classification", (df_a['uspc_class']))   


df_a['Percent Allowance f'] = (100. * df_a['allowance'])
df_a['Percent Allowance f'] = (df_a['Percent Allowance f'].map('{:.0f}%'.format))
cpc_allow = df_a.loc[df_a['uspc_class'] == option_c, 'Percent Allowance f'].values[0]


'**You selected:** ', option_c   
'**The probability that your patent will be approved with 2 years is:**', cpc_allow
