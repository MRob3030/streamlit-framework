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

df_class_s = pd.read_csv('Allow_class.csv')
df_class_top = pd.read_csv('Allow_prob_top3.csv')

st.title("Will My Patent Be Granted?")


            
st.write("The U.S. Patent and Trademark office publishes datasets including 11 million patent applications. This includes all applications from 1996 to 2018. When each patent application is filed it is assigned to a technology area and classification code. These features were used to create a prediction of the probability of the application being granted based on historical trends. ")


st.write('Select a technology area for your application:')



        
option_tech = st.selectbox("Technology", (df['TC']))             



df['Percent Allowance f'] = (100. * df['Percent Allowance'])
df['Percent Allowance f'] = (df['Percent Allowance f'].map('{:.0f}%'.format))
tech_allow = df.loc[df['TC'] == option_tech, 'Percent Allowance f'].values[0]


'**You selected:** ',  option_tech 
'**The probability that your patent will be approved is:**', tech_allow


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

bars.encoding.x.title = 'Technology'
bars.encoding.y.title = 'Granted Patent Probability'

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
).configure_axisX(labelAngle = 45)

st.altair_chart(c, use_container_width=True)


st.write("The U.S. Patent and Trademark office uses classification codes to sort applications by technology area. Codes that begin with 'D' refer to Design Patent. The remaining numerical codes encompass all other technologies.  ")

'''
 002-028   Apparel and Textiles 
 
 172       Earth Working
 
 530-588   Chemistry
 
 700-726   Data processing: measuring, calibrating, or testing
 
 PLT       Plants
 
 
 '''


#option_au = st.selectbox("Art Unit", (df_a['examiner_art_unit']))   
option_c = st.selectbox("Classification", (df_class_s['uspc_class']))   

'**You selected USPC class:** ', option_c   

df_class_top['Percent Allowance f'] = (100. * df_class_top['allowance'])
df_class_top['Percent Allowance f'] = (df_class_top['Percent Allowance f'].map('{:.0f}%'.format))
cpc_allow = df_class_top.loc[df_class_top['uspc_class'] == option_c, 'Percent Allowance f'].values[0]


df_b = df_class_top.loc[df_class_top['uspc_class'] == option_c].set_index('top_au')

best_au = df_b[['examiner_art_unit', 'Percent Allowance f', 'allowance']]
#best_au
au1 = best_au.iloc[0, 0]
au_p = best_au.iloc[0, 1]
au_2 = best_au.iloc[0, 2]


df_all = df_a.loc[df_a['uspc_class'] == option_c]
df_b['average_allow'] = df_all['allowance'].mean()

avg_class = 100. * df_b['average_allow'].iloc[0]
avg_class_f =  ('{:.0f}%').format(avg_class)

st.spinner()
with st.spinner(text='Calculating...'):
    time.sleep(3)
    st.success('Done')

'**The probability that your patent will be approved for any Art Unit is:**', avg_class_f



'**The best chance it will be approved is for Art Unit:**', au1, '**with an approval of:**', au_p

ratio = (100. * au_2) / avg_class
ratio_f = ('{:.1f}x').format(ratio)

'**This represent an improvement of:**', ratio_f, '**above the average art unit**'


brush = alt.selection(type='interval', encodings=['x'])

bars2 = alt.Chart(df_b).mark_bar().encode(
    x='examiner_art_unit',
    y='allowance',
    opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
).add_selection(
    brush
)


bars2.encoding.x.title = 'Examiner Art Unit'
bars2.encoding.y.title = 'Granted Probability'

line2 = alt.Chart().mark_rule(color='firebrick').encode(
    y='average_allow',
    size = alt.SizeValue(3)
).transform_filter(
    brush
)

d = alt.layer(bars2, line2, data=df_b).configure_title(fontSize=20).properties(

    title='Top 3 Art Units for Granted Patents',
    width=125,
    height=300).configure_axis(
    labelFontSize = 14,
    titleFontSize = 14
   ).configure_axisX(labelAngle = 0)

'''


'''

st.altair_chart(d, use_container_width=True)

