import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import altair as alt
import datetime
import time
from vega_datasets import data

#Load data
st.title('covid-19')

DATA_URL = ('owid/dataset_covid_world.csv')
@st.cache(allow_output_mutation=True)

def load_data():
    data = pd.read_csv(DATA_URL)
    data['date'] = pd.to_datetime(data['date'],format='%Y/%m/%d' ).dt.strftime('%Y-%m-%d')
    return data

#Load rows of data into the dataframe.
df = load_data()
st.write(df)

df_europe = df.loc[df['continent']== 'Europe']
all_country = df_europe['location'].unique()
# bar chart
filter_data = df[(df['date'] >= '2020-06-21') & (df['location']== 'France')].set_index("date")

st.markdown( "France data")

st.bar_chart(filter_data[['total_deaths']])


#widgets
subset_data = df_europe

### multiselect
country_name_input = st.multiselect(
'Country name',
df_europe.groupby('location').count().reset_index()['location'].tolist())

df_all_country = pd.DataFrame({'location':country_name_input})


df_chart = pd.merge(df_europe,df_all_country,on='location')

chkbox = st.checkbox("All countries")

st.subheader('Total declared case per countries')

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





##linechart
#total_cases_graph =alt.Chart(subset_data).transform_filter(
#    alt.datum.total_cases > 0
#).mark_line().encode(
#    x=alt.X('date', type='nominal'),
#    y=alt.Y('total_cases'),
#    color=color,
#    tooltip = 'sum(total_cases)',
#).properties(
#    width=1000,
#    height=400,
#).configure_axis(
#    labelFontSize=17,
#    titleFontSize=20
#)




#st.altair_chart(total_cases_graph)



##selectbox widgets
metrics =['total_cases','new_cases','total_deaths','new_deaths','total_cases_per_million','new_cases_per_million']

cols = st.selectbox('Covid metric to view', metrics)

#let's...
if cols in metrics:
    metric_to_show_in_covid_Layer = cols

##map

#variable...
date = datetime.date(2020,1,1)

#set...
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

#create...
covidLayer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    pickable=False,
    opacity=0.3,
    stroked=True,
    filled=True,
    radius_scale=10,
    radius_min_pixels=5,
    radius_max_pixels=60,
    line_width_min_pixels=1,
    get_position=["longitude", "latitude"],
    get_radius=metric_to_show_in_covid_Layer,
    get_fill_color=[252, 136, 3],
    get_line_color=[255,0,0],
    tooltip="test test",
)

#create...
r = pdk.Deck(
    layers=[covidLayer],
    initial_view_state=view,
    map_style="mapbox://styles/mapbox/light-v10",
)

#create...
subheading = st.subheader("")

#render...
map = st.pydeck_chart(r)

#update...
#for i in df['date']:
    #increment..
    #date += datetime.timedelta(days=1)

    #update..
    #covidLayer.data = df[df['date'] == date.isoformat()]

    #update..
    #r.update()

    #render..
    #map.pydeck_chart(r)

    #update..
    #subheading.subheader("%s on : %s" % (metric_to_show_in_covid_Layer, date.strftime("%B %d, %Y")))

    #wait..
    #time.sleep(0.2)