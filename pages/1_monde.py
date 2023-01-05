import streamlit as st
import streamlit_folium
from streamlit_folium import folium_static
import pandas as pd
import numpy as np 
import matplotlib
import plotly 
import folium
from folium.plugins import MarkerCluster
from folium.plugins import HeatMap
import datetime
import pydeck as pdk
import altair as alt
import time
from vega_datasets import data
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



df = pd.read_csv('.\owid\dataset_covid_world.csv')


covid_final = df.loc[df['date'] == df['date'].max(), ['country','latitude','longitude','total_cases_per_million','total_vaccinations_per_hundred','total_deaths_per_million','new_cases']]
st.markdown("<h1 style='text-align: center; color: #ff634d;'><strong><u>Covid-19 dans le monde 🌍</u></strong></h1>", unsafe_allow_html=True)
st.markdown("Cette Web App est un dashboard sur le Covid-19 avec comme source de données Our World In Data (OWID)", unsafe_allow_html=True)

st.sidebar.markdown("<h1 style='text-align: center; color: #aaccee;'><strong><u>Covid-19 Dashboard</u></strong></h1>", unsafe_allow_html=True)

nb_cas = df.loc[df['date'] == df['date'].max(), 'total_cases_per_million'].sum()
nb_vaccin = df.loc[df['date'] == df['date'].max(), 'total_vaccinations_per_hundred'].sum()
nb_mort = df.loc[df['date'] == df['date'].max(), 'total_deaths_per_million'].sum()

#st.sidebar.write("<div style='background-color : #FFE033;margin-left : 10px'> <h2 style='margin-left:10px;margin-bottom:10px'>Nombre total de cas (en million) :</h2><h2 style='margin-left:15px;padding-bottom:10px'><strong>",str(nb_cas),"</strong></h2></div>", unsafe_allow_html=True)
#st.sidebar.write("<div style='background-color : #6FCF10;margin-left : 10px'> <h2 style='margin-left:10px;margin-bottom:10px'>Nombre total de vaccination (en millier) :</h2><h2 style='margin-left:15px;padding-bottom:10px'><strong>",str(nb_vaccin),"</strong></h2></div>", unsafe_allow_html=True)
#st.sidebar.write("<div style='background-color : #CF1010;margin-left : 10px'> <h2 style='margin-left:10px;margin-bottom:10px'>Nombre total de mort (en million) :</h2><h2 style='margin-left:15px;padding-bottom:10px'><strong>",str(nb_mort),"</strong></h2></div>", unsafe_allow_html=True)

#carte sur le nombre de vaccination
m = folium.Map(tiles='Stamen Terrain',min_zoom=1.5)
url='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'
folium.Choropleth(
geo_data=country_shapes,
min_zoom=2,
name='Covid-19',
data=covid_final,
columns=['country','total_vaccinations_per_hundred'],
key_on='feature.properties.name',
fill_color='PuBuGn',
nan_fill_color='black',
legend_name='Nombre de vaccination',
).add_to(m)

dfn= df.loc[df['date'] == df['date'].max(), ['country','total_cases','total_vaccinations','total_deaths']]
dfn = dfn.groupby('country')['total_cases','total_vaccinations','total_deaths'].sum().sort_values(by='total_cases',ascending=False)

# map nouveau cas
m4 = folium.Map(tiles='Stamen Terrain',min_zoom=1.5)
url='https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
country_shapes = f'{url}/world-countries.json'
folium.Choropleth(
geo_data=country_shapes,
min_zoom=2,
name='Covid-19',
data=covid_final,
columns=['country','total_cases_per_million'],
key_on='feature.properties.name',
fill_color='YlOrRd',
nan_fill_color='black',
legend_name='Cas confirmés',
).add_to(m4)

dfn

st.write('NOMBRE DE CAS CONFIRMÉS DANS LE MONDE - ',nb_cas)
st.write('NOMBRE DE MORT CONFIRMÉES DANS LE MONDE - ',nb_mort)
st.write('NOMBRE DE VACCINATIONS DANS LE MONDE - ',nb_vaccin)


st.sidebar.subheader('Analyses à travers une carte - Folium')

st.subheader("Vue d'enssemble sur l'évolution du Covid-19 dans le monde")    

select = st.sidebar.selectbox('Choissisez le type de carte',['Cas confirmés (en millions)','Vaccinations (en milliers)','Morts (en millions)'],key='1')



if not st.sidebar.checkbox("Cacher la carte",True):
    
    if select == "Cas confirmés (en millions)": 
        folium_static(m4,width=1000,height=600)
        

    elif select == "Vaccinations (en milliers)":
        
        folium_static(m,width=1000,height=600)
        
        
    else:
        m2 = folium.Map(tiles='StamenToner',min_zoom=1.5)
        deaths=covid_final['total_deaths_per_million'].astype(float)
        lat=covid_final['latitude'].astype(float)
        long=covid_final['longitude'].astype(float)
        
        m2.add_child(HeatMap(zip(lat,long,deaths),radius=0))
        folium_static(m2,width=1000,height=600)

col1,col2,col3 = st.columns(3,gap='large')
with col1:
    fig = px.bar(df[((df['location']== 'World'))], y='new_cases',x='date',color='location')
    fig.update_layout(title='Nouveaux cas confirmés',
        xaxis_title='',template="plotly_dark",
        yaxis_title='',
        height=200,
        width=300,
        showlegend=False,   
    )
    st.plotly_chart(fig)
with col2:
    fig = px.bar(df[((df['location']== 'World'))], y='new_deaths',x='date',color='location')
    fig.update_layout(title='Nombre de décés ',
        xaxis_title='',template="plotly_dark",
        yaxis_title='',
        height=200,
        width=300,
        showlegend=False,
    )    
    st.plotly_chart(fig) 
with col3:
    fig = px.bar(df[((df['location']== 'World'))], y='new_vaccinations',x='date',color='location')
    fig.update_layout(title='Nombre de vaccination ',
        xaxis_title='',template="plotly_dark",
        yaxis_title='',
        height=200,
        width=300,
        showlegend=False,
        
    )
    st.plotly_chart(fig) 

#dataframe pour chart 1

df1 = df.loc[df['location'] == 'France', ['location','weekly_hosp_admissions','date']]

df1.head(10)


def get_chartAll(data,variable):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = total_cases_graph = alt.Chart(data[data['location'] == data['location']]).mark_circle().encode(
    ).mark_line().encode(
        x=alt.X('date', type='nominal'),
        y=alt.Y(variable),
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
            y=variable,
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip('location',title="Pays"),
                alt.Tooltip("date", title="Date"),
                alt.Tooltip(variable, title="Hospitalisation hebdomadaire"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()

def get_chart_icu(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = total_cases_graph = alt.Chart(data[data['location'] == data['location']]).mark_circle().encode(
    ).mark_line().encode(
        x=alt.X('date', type='nominal'),
        y=alt.Y('icu_patients'),
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
            y="icu_patients",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip('location',title="Pays"),
                alt.Tooltip("date", title="Date"),
                alt.Tooltip('icu_patients', title="Hospitalisation en soin intensifs"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


st.sidebar.subheader('Analyse à travers des graphes - Plotly')

chart = get_chartAll(df[((df['location']== 'United States')|(df['location']== 'France')|(df['location']== 'Canada')|(df['location']== 'Italy')|(df['location']== 'United Kingdom')|(df['location']== 'Spain'))],'weekly_hosp_admissions')  
chart2 = get_chart_icu(df[((df['location']== 'United States')|(df['location']== 'France')|(df['location']== 'Canada')|(df['location']== 'Italy')|(df['location']== 'United Kingdom')|(df['location']== 'Spain'))])
if not st.sidebar.checkbox("Cacher les graphe",True):
    
    st.subheader("Nombre d'hospitalisations hebdomadaire dans le monde")    

    st.altair_chart(
        (chart).interactive(),
        use_container_width=True  
    )

    st.subheader("Nombre d'hospitalisations en soin intensifs dans le monde")  
    st.altair_chart(
        (chart2).interactive(),
        use_container_width=True  
    )
df10 = df[((df['location']== 'World'))]
dfc = df10.groupby('location')['date','total_vaccinations','new_vaccinations_smoothed'].max().sort_values(by='total_vaccinations',ascending=False).reset_index()

df_map = filter_data = df[(df['date'] >= '2020-06-21') & (df['location']== 'France')].set_index("date")

##selectbox widgets
metrics =['total_cases','new_cases','total_deaths','new_deaths','total_cases_per_million','new_cases_per_million']

cols = st.selectbox('Choix type de données', metrics)

#let's...
if cols in metrics:
    metric_to_show_in_covid_Layer = cols

##map

#variable...
date = datetime.date(2020,2,15)

#set...
view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)


#create...
covidLayer = pdk.Layer(
    "ScatterplotLayer",
    data=df_map,
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
for i in df['date']:
    #increment..
    date += datetime.timedelta(days=1)

    #update..
    covidLayer.data = df[df['date'] == date.isoformat()]

    #update..
    r.update()

    #render..
    map.pydeck_chart(r)

    #update..
    subheading.subheader("%s on : %s" % (metric_to_show_in_covid_Layer, date.strftime("%B %d, %Y")))

    #wait..
    time.sleep(0.5)
# A neat combination of st.columns with metrics.

#empty map
#world_map= folium.Map(tiles="cartodbpositron")
#marker_cluster = MarkerCluster().add_to(world_map)
#for each coordinate, create circlemarker of user percent
#for i in range(df.location.nunique()):
#        lat = df.iloc[i]['latitude']
#        long = df.iloc[i]['longitude']
#        radius=5
#        popup_text = """Country : {}<br>
#                    Total de cas : {}<br>"""
#        popup_text = popup_text.format(df.iloc[i]['country'],
#                                   df.iloc[i]['total_cases']
#                                   )
#        folium.CircleMarker(location = [lat, long], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
#show the map
#st.markdown(world_map._repr_html_(), unsafe_allow_html=True)
#start_date = datetime.strptime("01/01/19", '%d/%m/%y')
#end_date = datetime.strptime("01/01/22", '%d/%m/%y')
#start_time = st.slider("",
#     min_value=start_date,
#     max_value=end_date,
#     format="DD/MM/YYYY"
#)
