import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import numpy as np 
import matplotlib
import plotly 
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
from datetime import datetime
import pydeck as pdk
import altair as alt
import time
from vega_datasets import data
import plotly.express as px


df = pd.read_csv('owid/dataset_covid_world.csv')

st.markdown("# Page Europe 🇪🇺")
st.sidebar.markdown("# Page Europe 🇪🇺")


df_europe = df.loc[df['continent']== 'Europe']
all_country = df_europe['location'].unique()

nb_cas = df_europe.loc[df['date'] == df['date'].max(), 'total_cases_per_million'].sum()
nb_vaccin = df_europe.loc[df['date'] == df['date'].max(), 'total_vaccinations_per_hundred'].sum()
nb_mort = df_europe.loc[df['date'] == df['date'].max(), 'total_deaths_per_million'].sum()

st.write('NOMBRE DE CAS CONFIRMÉS EN EUROPE - ',nb_cas)
st.write('NOMBRE DE MORT CONFIRMÉES EN EUROPE - ',nb_mort)
st.write('NOMBRE DE VACCINATIONS EN EUROPE - ',nb_vaccin)

#widgets
subset_data = df_europe

### multiselect
country_name_input = st.multiselect(
'Choix du pays',
df_europe.groupby('location').count().reset_index()['location'].tolist())


df_all_country = pd.DataFrame({'location':country_name_input})



df_chart = pd.merge(df_europe,df_all_country,on='location')


chkbox = st.checkbox("Tous les pays")

st.subheader('Total des cas déclarés par pays')

def get_chartCountryEU(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = total_cases_graph = alt.Chart(data).mark_circle().encode(
    ).mark_line().encode(
        x=alt.X('date', type='nominal'),
        y=alt.Y('total_cases'),
        color='location',
    ).properties(
        width=1000,
        height=600,
    )
    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="date",
            y="total_cases",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip('location',title='Country'),
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("total_cases", title="Total cases"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

def get_chartAllEU(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = total_cases_graph = alt.Chart(data[data['location'] == data['location']]).mark_circle().encode(
    ).mark_line().encode(
        x=alt.X('date', type='nominal'),
        y=alt.Y('total_cases'),
        color='location',
    ).properties(
        width=1000,
        height=600,
    )
    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="date",
            y="total_cases",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip('location',title='Country'),
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("total_cases", title="Total cases"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

def get_chartAll(data):

    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = total_cases_graph = alt.Chart(data[data['location'] == data['location']]).mark_circle().encode(
    ).mark_line().encode(
        x=alt.X('date', type='nominal'),
        y=alt.Y('stringency_index'),
        color='location',
    ).properties(
        width=1000,
        height=600,
    )
    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="date",
            y="stringency_index",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip('location',title="Pays"),
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("stringency_index", title="Niveaux de restriction"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

def get_chartCountry(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = total_cases_graph = alt.Chart(data).mark_circle().encode(
    ).mark_line().encode(
        x=alt.X('date', type='nominal'),
        y=alt.Y('stringency_index'),
        color='location',
    ).properties(
        width=1000,
        height=600,
    )
    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="date",
            y="stringency_index",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip('location',title='Pays'),
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("stringency_index", title="Niveaux de restriction"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

if chkbox == False:
   chart = get_chartCountryEU(df_chart) 
   st.altair_chart(
    (chart).interactive(),
    use_container_width=True
    )

else:
   chart = get_chartAllEU(df_europe)
   st.altair_chart(
        (chart).interactive(),
        use_container_width=True  
   )


st.subheader('Niveaux de restrictions mis en place par pays (0 à 100)')



if chkbox == False:
    chart = get_chartCountry(df_chart)
    st.altair_chart(
        (chart).interactive(),
        use_container_width=True  
    )
else:
    chart = get_chartAll(df_europe)
    st.altair_chart(
        (chart).interactive(),
        use_container_width=True  
    )

