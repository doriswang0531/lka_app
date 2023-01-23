# Sri Lanka Small Tanks Data Analysis
# data source: UNDP small tanks databse

### import modules
from matplotlib import container
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import os

st.set_page_config(page_title='Sri Lanka Small Tanks Data Analysis Result', page_icon=':tada', layout='wide')
st.header('Sri Lanka Small Tanks Data Analysis')
st.write('_data source: UNDP small tanks database_')
st.info('This app was made for an internal presentation of descriptive analysis on Small tanks in Sri Lanka to South Asia Water team and Country office team. Last modified: 2022/10, by Qiao Wang')
st.write('Researh questions:')
st.write(
    """
    - Where are the tanks (reservoirs) in the country? 
    - How many are functional? What is their status? 
    - Which of the tanks are both non-functional and exposed to drought situation? 
    - How does tank functionality compare to population pressures and poverty? 
    """
    )

### --- LOAD DATASET
tank_csv_file = 'undp_small_tanks_merged.csv'
asc_csv_file = 'undp_small_tanks_merged_asc.csv'
dist_csv_file = 'undp_small_tanks_merged_dist.csv'
poverty_csv_file = 'HIES_poverty_agri.csv'
tank_df = pd.read_csv(os.path.join(tank_csv_file), encoding='utf-8')
tank_df = tank_df.drop(index=(tank_df.loc[tank_df['merge_survey']=='Using only (2)']).index)

### --- MAPS


### --- BACKGROUND
st.markdown('#### Introduction')
st.write('##')
st.write(
    """
    - 21,745 small tanks were mapped in dry zone of Sri Lanka, by UNDP together with the Ministry of Disaster Management and Department of Agrarian Development.
    - Information of 14,515 small tanks (68%) were collected in the form of survey questionnaire.
    - 74.5% of mapped small tanks are DAD tank, 24.9% are forest tank, tank of Irrigation Department and Mahaweli are less than 0.1%.
    """
    )

### --- PIE CHART: TANK OWNERSHIP
own_df = tank_df.groupby(['tankownership_map'])[['map_id']].count().rename(columns={'map_id':'num_tanks_map'})
own_df1 = tank_df[tank_df['merge_survey']=="Matched (3)"].groupby(['tankownership_map'])[['map_id']].count().rename(columns={'map_id':'num_tanks'})
own_df2 = pd.merge(own_df, own_df1, on=['tankownership_map'], how='inner')

own_pie = px.pie(values=own_df['num_tanks_map'], names=own_df.index, color_discrete_sequence=px.colors.qualitative.Pastel, title='Tank Ownership (N=21,745)')
own_pie.update_traces(textposition='inside', textinfo='percent+label')
own_pie.update_layout(height=400)

### --- DATAFRAME: TANK DATA COLLECTION RATE
# percent of tanks that were surveyed
own_df2.loc['Total'] = own_df2.sum()
own_df2['collection rate (%)'] = round(own_df2['num_tanks']/own_df2['num_tanks_map']*100, 1)
own_df2.columns=['N. tanks mapped', 'N. tanks in data collection', 'collection rate (%)']

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.plotly_chart(own_pie, height=400)

    with right_column:
        st.write('##')
        st.write('Number of Tanks Mapped and Surveyed')
        st.dataframe(own_df2)


### --- PIE CHART: TANK FUNCTIONALITY
func_df = tank_df.groupby(['functionality'])['map_id'].count()
func_pie = px.pie(values=func_df.values, names=func_df.index, color=func_df.values, color_discrete_sequence=px.colors.qualitative.Safe, title='Tank Functionality (N=14,515)')
func_pie.update_traces(textposition='inside', textinfo='percent+label', insidetextorientation='horizontal')

st.write('---')
st.markdown('#### Descriptive Analysis') 
st.markdown('##### 1 Functionality')
st.plotly_chart(func_pie)

### --- BAR CHART: ESTABLISHING HISTORY
est_year_df = tank_df.groupby(['est_year'])['map_id'].count().reset_index().rename(columns={'map_id':'num_tanks'})
color_discrete_sequence = ['#609cd4']*len(est_year_df)
est_bar = px.bar(est_year_df, y='num_tanks', text_auto='.2s', title='Number of Tanks by Establishing Year', 
                labels={ 'index': 'Establishing year', 'num_tanks': 'Number of tanks' }, 
                color_discrete_sequence=color_discrete_sequence)
for idx in range(len(est_bar.data)):
    est_bar.data[idx].x = ["Before 1970","1971 - 1980", "1981 - 1990", "1991 - 2000", "2001 - 2010", "2011 - 2020"]


func_est_year_df = round(tank_df.groupby(['est_year', 'functionality'])['map_id'].count()/tank_df.groupby(['est_year'])['map_id'].count()*100, 1).reset_index().rename(columns={'map_id':'pct_tanks'})
func_est_bar = px.bar(func_est_year_df, x='est_year', y='pct_tanks', color='functionality', title='Number of Tanks by Establishing Year and Functionality', text_auto=True,
             labels={ 'est_year': 'Establishing year', 'pct_tanks': 'Percent of tanks (%)' }, color_discrete_sequence=px.colors.qualitative.Safe )
for idx in range(len(func_est_bar.data)):
    func_est_bar.data[idx].x = ["Before 1970","1971 - 1980", "1981 - 1990", "1991 - 2000", "2001 - 2010", "2011 - 2020"]
func_est_bar.update_traces(textangle=0, textposition='inside')

st.write('---')
st.markdown('##### 2 Establishing history')
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.plotly_chart(est_bar)
    with right_column:
        st.plotly_chart(func_est_bar)        


### --- TANK INNOVATIONS
reno_df = tank_df.groupby(['_3tankrehabilitatedrenovat', 'functionality'])['map_id'].count().reset_index().rename(columns={'map_id':'num_tanks'})
reno_df['_3tankrehabilitatedrenovat'] = reno_df['_3tankrehabilitatedrenovat'].astype(str).replace({'0.0':'No', '1.0':'Yes'})

reno_bar = px.bar(reno_df, x='_3tankrehabilitatedrenovat', y='num_tanks', color='functionality', barmode='group', text_auto=True, title='Number of Tanks by Functionality, Renovation', 
             labels={ '_3tankrehabilitatedrenovat': 'Renovated in the last five year', 'num_tanks': 'Number of tanks' }, color_discrete_sequence=px.colors.qualitative.Safe)

func_reno_df = round(tank_df.groupby(['_3tankrehabilitatedrenovat', 'functionality'])['map_id'].count()/tank_df.groupby(['_3tankrehabilitatedrenovat'])['map_id'].count()*100, 1).reset_index().rename(columns={'map_id':'pct_tanks'})
func_reno_df['_3tankrehabilitatedrenovat'] = reno_df['_3tankrehabilitatedrenovat'].astype(str).replace({'0.0':'No', '1.0':'Yes'})

func_reno_bar = px.bar(func_reno_df, x='_3tankrehabilitatedrenovat', y='pct_tanks', color='functionality', text_auto=True, title='Percent of Tank by Functionality, Renovation', 
             labels={ '_3tankrehabilitatedrenovat': 'Renovated in the last five year', 'pct_tanks': 'Percent of tanks (%)' }, color_discrete_sequence=px.colors.qualitative.Safe)

st.write('---')
st.markdown('##### 3 Renovated in the last five years')
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.plotly_chart(reno_bar)

    with right_column:
        st.plotly_chart(func_reno_bar)
st.write('The age of the tanks does not immediately correlate with the level of functionality.')

### --- BAR CHART: TANK UTILIZATION (MULTIPLE CHOICES)
utili_df = round(tank_df[['_4_1irrigatedagriculture', '_4_2fishing', '_4_3livestock', '_4_4daytodayuse', '_4_5smallscaleindustries', '_4_6environmentaluse', '_4_7ecotourism']].mean()*100, 2).reset_index()
utili_df.columns = ['utilization', 'pct_tank']
utili_df = utili_df.replace({'_4_1irrigatedagriculture':'Irrigation', 
                             '_4_2fishing':'Fishing', 
                             '_4_3livestock':'Livestock', 
                             '_4_4daytodayuse':'Day-to-day use', 
                             '_4_5smallscaleindustries':'Samll scale industries', 
                             '_4_6environmentaluse':'Environment use', 
                             '_4_7ecotourism':'Ecotourism'})

uti_bar = px.bar(utili_df, x=utili_df['utilization'], y='pct_tank', color='utilization', text_auto='.2s', title='Percent of Tanks by Utilization (multiple choices)', 
             labels={'utilization':'', 'pct_tank': 'Percent of tanks (%)' }, color_discrete_sequence=px.colors.qualitative.Pastel)


### --- PIE CHART: TANK UTILIZATION (MULTIPLE CHOICES)
uti_df = tank_df.groupby('tank_utili')['map_id'].count()
uti_pie = px.pie(values=uti_df.values, names=uti_df.index)
uti_pie.update_layout(title="Tank Utilization (top choices)")
uti_pie.update_traces(textposition='inside', textinfo='percent+label')

### --- DATAFRAME: TANK UTILIZAITON (TOP CHOICES)
#  list of utilization, freq, pct
index = ['irrigation only', 'irrigation-daytoday', 'irrigation-livestock-daytoday', 'irrigation-fishing-livestock-daytoday', 'irrigation-livestock', 'irrigation-fishing-livestock'] 
freq = [4690, 1724, 1329, 989, 903, 500 ]
pct = [21.56, 7.93, 6.11, 4.55, 4.15,2.3]
dict = {'N. tanks': freq, 'Pct. tanks (%)': pct} 
utility_df = pd.DataFrame((dict), index=index)

st.write('---')
st.markdown('##### 4 Tank utilization')
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.plotly_chart(uti_bar)
    with right_column:
        st.write('##')
        st.write('Tank Utilization (Top choices)')
        st.write('_among 14,515 small tanks_')
        st.dataframe(utility_df)
st.write('The largest usage of tanks is for irrigation only.')


### --- SPATIAL DISTRIBUTION: TANK UTILIZATION
image1 = Image.open('maps/tank_irrigation.jpg')
image2 = Image.open('maps/tank_agri.jpg')
image3 = Image.open('maps/tank_agri_day.jpg')

st.write('---')
st.markdown('##### 5 Tank spatial distribution by utilization')
with st.container():
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.write('Irrigation Only')
        st.image(image1, width=350)
    with middle_column:
        st.write('Agriculture (Irrigation/Fishing/Livestock')
        st.image(image2, width=400)
    with right_column:
        st.write('Agriculture and Day-to-day')
        st.image(image3, width=400)
