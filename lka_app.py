# Sri Lanka Small Tanks Data Analysis
# data source: Mapping small tank in the dry zone of Sri Lanka (UNDP and DAD)

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
        st.write('Agriculture (Irrigation/Fishing/Livestock)')
        st.image(image2, width=400)
    with right_column:
        st.write('Agriculture and Day-to-day')
        st.image(image3, width=400)
        
 ### --- DATAFRAME: FUNCTIONALITY BY DISTRICT
dist_df = pd.read_csv(os.path.join('dist_csv_file'), encoding='utf-8')
dist_df = dist_df.dropna(subset=['districtname'])

dist_df1 = dist_df[['districtname', 'dist_pop', 'dist_func', 'dist_damaged', 'dist_nonfunc']].sort_values(by=['dist_func']).reset_index(drop=True)
dist_df1.index = dist_df1.index + 1
dist_df1.columns = ['District', 'Population', 'Pct. tanks functioning', 'Pct. tanks damaged', 'Pct. tanks non-functioning']

### --- BAR CHART
color_discrete_sequence = ['#5f4690']*len(dist_df1)
func_bar = px.bar(dist_df1, x='District', y='Pct. tanks functioning', text_auto='.2S', title='Percent of Functioning Tanks in District (%) ', 
                labels={ 'District': 'District', 'Pct. tanks functioning': 'Percent of tanks (%)' }, color_discrete_sequence=color_discrete_sequence)

### --- DATAFRAME: PERCENT OF TANKS BY FUNCTIONALITY
st.write('---')
st.markdown('##### 6 District Level analysis') 
with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.write('Percent of tanks in district with the following status of tank functionality (%)')
        st.dataframe(dist_df1)
    with right_column:
        st.plotly_chart(func_bar)


### --- DATAFRAME: PERCENT OF POPULATION
dist_df2 = dist_df[['districtname', 'dist_pop', 'dist_pop_func', 'dist_pop_damaged', 'dist_pop_nonfunc']].sort_values(by=['dist_pop_func']).reset_index(drop=True)
dist_df2.columns = ['District', 'Population', 'Access to functioning tank', 'Access to damaged tank', 'Without access']


### --- BAR CHART
color_discrete_sequence = ['#1d6a96']*len(dist_df2)
pop_func_bar = px.bar(dist_df2, x='District', y='Access to functioning tank', text_auto='.2S', title='Population with Access to Functioning Tank in District (%) ', 
                    labels={ 'District': 'District', 'Access to functioning tank': 'Population access (%)' }, color_discrete_sequence=color_discrete_sequence)

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.write('Population access to functioning tank in district (%)')
        st.dataframe(dist_df2)
    with right_column:
        st.plotly_chart(pop_func_bar)
st.write('Mallaitivu District with more than 70% population relied on agriculture, but only 21% are covered by a functional tank')

### --- CORRELATION ANALYSIS: POVERTY
dist_poverty_df = pd.read_csv(os.path.join(poverty_csv_file), encoding='utf-8')
dist_poverty_df.columns=['districtname', 'Poverty rate 2002', 'Poverty rate 2012', 'District', 'Pct. HH in agriculture occupation', 'Pct. Population in agriculture occupation']
dist_poverty_df = pd.merge(dist_df2, dist_poverty_df, on=['District'], how='inner').reset_index(drop=True)

color_discrete_sequence = ['#99c945']*len(dist_poverty_df)
dist_agri_sca = px.scatter(dist_poverty_df, x='Access to functioning tank', y='Pct. Population in agriculture occupation', size='Population', text='District', 
                 title='Agriculture Occupation (%)', color_discrete_sequence=color_discrete_sequence, trendline='ols',
                 labels={ 'Pct. Population in agriculture occupation': 'HIES population with agriculture occupation 2016 (%)', 
                 'Access to functioning tank': 'Population with access to functioning tank (%)', 
                 'Population': 'Population' })
dist_agri_sca.update_traces(textposition='top center')


color_discrete_sequence = ['#cc61af']*len(dist_poverty_df)
dist_pov_sca = px.scatter(dist_poverty_df, x='Access to functioning tank', y='Poverty rate 2012', size='Population', text='District', 
                 title='Poverty (%)', color_discrete_sequence=color_discrete_sequence, trendline='ols',
                 labels={ 'Poverty rate 2012': 'HIES poverty head count 2012 (%)', 
                 'Access to functioning tank': 'Population with access to functioning tank (%)', 
                 'Population': 'Population' })
dist_pov_sca.update_traces(textposition='top center')


with st.container():
    st.write('---')
    st.markdown('##### 7 Tank Access, Agriculture Engagement and Poverty') 
    left_column, right_column = st.columns(2)
    with left_column:
        st.plotly_chart(dist_agri_sca)
    with right_column:
        st.plotly_chart(dist_pov_sca)


### --- SPATIAL DISTRIBUTION: TANK FUNCTIONALITY
image4 = Image.open('maps\dist_pop_agri.jpg')
image5 = Image.open('maps\dist_pop_func.jpg')

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.write('Population with Occupation in Agriculture Industry (%, HIES 2016)')
        st.image(image4, caption='', width=600)
        st.write('##')

    with right_column:
        st.write('Population with Access to Functioning Tank (%)')
        st.image(image5, caption='', width=600)
        st.write('##')

st.write('''
    - High non-accessibility (more than 60%) to functional tanks for DSDs in northern districts (Kilinochchi, Mullaitivu, Mannar, Vavunlya,  Batticaloa)​
    - Dark brown shades show the DSDs with both high non-access and  experienced high level of drought frequency​
''')

### --- DSD LEVE ANALYSIS
st.write('---')
st.markdown('##### 8 DSD level analysis') 

asc_df = pd.read_csv(os.path.join(asc_csv_file), encoding='utf-8')
asc_df = asc_df.dropna(subset=['adm3_en', 'adm2_en'])
asc_df = asc_df.drop(index=(asc_df.loc[asc_df['adm2_en']=='Nuwara Eliya']).index)
asc_df = asc_df.drop(index=(asc_df.loc[asc_df['adm2_en']=='Ratnapura']).index)
asc_df = asc_df.drop(index=(asc_df.loc[asc_df['adm2_en']=='Jaffna']).index)
asc_df = asc_df.rename(columns={'adm2_en':'District', 'adm3_en':'DSD'})

asc_pov_df = pd.read_csv(os.path.join(poverty_csv_file), encoding='utf-8')
asc_pov_df = asc_pov_df.rename(columns={'ADM2_EN':'District', 'ADM3_EN':'DSD'})
mask_df = asc_df[['District', 'DSD', 'asc_pop_func', 'asc_pop_damaged', 'asc_pop_nonfunc']]
mask_df = pd.merge(mask_df, asc_pov_df, on=['DSD'], how='inner').reset_index(drop=True)
mask_df = mask_df.dropna(subset=['asc_pop_func'])
mask_df = round(mask_df[['District_x', 'DSD', 'asc_pop_func', 'asc_pop_damaged', 'asc_pop_nonfunc', 'Estimated headcount index (%)']], 2)
mask_df.columns=['District', 'DSD', 'Access to functioning tank (%)', 'Access to damaged tank (%)', 'With no access to functioning tank (%)', 'Estimated poverty headcount index (%)']

district = asc_df['District'].unique().tolist()
district_selection = st.multiselect('District:', 
                                    district, 
                                    default=district)

mask= mask_df['District'].isin(district_selection)
number_of_result = mask_df[mask].shape[0]

asc_bar = px.bar(mask_df[mask], x='DSD', y='Access to functioning tank (%)', text_auto='.2s',
                color_discrete_sequence=['#f63366']*len(mask_df[mask]),
                template='plotly_white')

with st.container():
    left_column, right_column = st.columns(2)
    with left_column:
        st.write('Access to Tank and Poverty Rate at DSD level')
        st.markdown(f'*Available results: {number_of_result}*')
        st.dataframe(mask_df[mask])
    with right_column:
        st.write('Population Access to Functioning Tank (%)')
        st.plotly_chart(asc_bar, use_container_width=True)

### --- SCATTER PLOT
color_discrete_sequence = ['#cc61af']*len(mask_df)
asc_pov_sca = px.scatter(mask_df, x='Access to functioning tank (%)', y='Estimated poverty headcount index (%)',  
                 title='Access to Functioning Tank and Poverty Rate', color_discrete_sequence=color_discrete_sequence, trendline='ols',
                 template='plotly_white')
asc_pov_sca.update_layout(height=800)


with st.container():
    left_column, middle_column, right_column = st.columns((2, 5, 2))
    with middle_column:
        st.write('##')
        st.plotly_chart(asc_pov_sca, use_container_width=True, height=800)

### --- BIVARIATE MAP
image6 = Image.open('asc_pop_nofunc.jpg')
image7 = Image.open('asc_pop_dro.jpg')
image8 = Image.open('asc_nonfunc_dro_biv.jpg')

with st.container():
    st.write('---')
    st.markdown('##### 10 DSD Bivariate Map') 
    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.write('Population with access to non-functional tank (%)')
        st.image(image6, caption='', width=600)
        st.write('##')
    with middle_column:
        st.write('Population living under severe drought (%, 2011-2020)')
        st.image(image7, caption='', width=600)
    with right_column:
        st.write('Access - Drought bivariate map')
        st.image(image8, caption='', width=600)
        st.write('##')
