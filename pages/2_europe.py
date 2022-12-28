import streamlit as st
<<<<<<< HEAD
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

df = pd.read_csv('.\owid\dataset_covid_world.csv')

st.markdown("# Page Europe 🇪🇺")
st.sidebar.markdown("# Page Europe 🇪🇺")


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

chart = get_chartAll(df.loc[df['continent']== 'Europe'])

st.altair_chart(
    (chart).interactive(),
    use_container_width=True  
)
=======

st.markdown("# Page Europe 🇪🇺")
st.sidebar.markdown("# Page Europe 🇪🇺")
>>>>>>> cc9f0f5 (ordering pages)
