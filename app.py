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
df = df.sort_values(by=['TC'], inplace=False)
df = df.reset_index()

df_a = pd.read_csv('Allow_prob_43k.csv')
df_a = df_a.sort_values(by=['uspc_class'], inplace= False)
df_a = df_a.reset_index()   

df_class = pd.read_csv('Allow_class.csv')
df_class = df_class.sort_values(by=['uspc_class'], inplace = False)
df_class = df_class.reset_index()   

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

c = alt.layer(bars, line, data=df).properties(
    width=125,
    height=700,
).configure_title().configure_axis(
    labelFontSize = 16,
    titleFontSize = 20
)
st.altair_chart(c, use_container_width=True)


st.write("The U.S. Patent and Trademark office uses classification codes to sort applications by technology area. Codes that begin with 'D' refer to Design Patent. The remaining numerical codes encompass all other technologies.  ")

'''
 002-028   Apparel and Textiles 
 
 172       Earth Working
 
 530-588   Chemistry
 
 702-726   Data processing: measuring, calibrating, or testing
 
 PLT       Plants
 
 
 '''


#option_au = st.selectbox("Art Unit", (df_a['examiner_art_unit']))   
option_c = st.selectbox("Classification", (df_class['uspc_class']))   


df_a['Percent Allowance f'] = (100. * df_a['allowance'])
df_a['Percent Allowance f'] = (df_a['Percent Allowance f'].map('{:.0f}%'.format))
cpc_allow = df_a.loc[df_a['uspc_class'] == option_c, 'Percent Allowance f'].values[0]





df_b = df_a.loc[df_a['uspc_class'] == option_c]
df_b['average_allow'] = df_b['allowance'].mean()
df_c = df_b[['examiner_art_unit', 'uspc_class', 'allowance', 'average_allow']]

avg_class = 100. * df_b['allowance'].mean()
avg_class_f =  ('{:.0f}%').format(avg_class)

'**You selected:** ', option_c   
'**The probability that your patent will be approved is:**', avg_class_f

df_c



brush = alt.selection(type='interval', encodings=['x'])

bars2 = alt.Chart(df_c).mark_bar().encode(
    x='examiner_art_unit',
    y='allowance',
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
).add_selection(
    brush
)

line2 = alt.Chart().mark_rule(color='firebrick').encode(
    y='average_allow',
    size = alt.SizeValue(3)
).transform_filter(
    brush
)

d = alt.layer(bars2, line2, data=df_c)
st.altair_chart(d, use_container_width=True)
