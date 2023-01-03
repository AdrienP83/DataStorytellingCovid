import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from datetime import datetime

st.markdown("# Page monde 🌍")
st.sidebar.markdown("# Page monde 🌍")


st.write("ici le premier graphe d'évolution du COVID dans le monde")

df = pd.read_csv('.\owid\dataset_covid_world.csv')

#empty map
world_map= folium.Map(tiles="cartodbpositron")
marker_cluster = MarkerCluster().add_to(world_map)
#for each coordinate, create circlemarker of user percent
for i in range(df.location.nunique()):
        lat = df.iloc[i]['latitude']
        long = df.iloc[i]['longitude']
        radius=5
        popup_text = """Country : {}<br>
                    Total de cas : {}<br>"""
        popup_text = popup_text.format(df.iloc[i]['country'],
                                   df.iloc[i]['total_cases']
                                   )
        folium.CircleMarker(location = [lat, long], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)
#show the map
st.markdown(world_map._repr_html_(), unsafe_allow_html=True)
start_date = datetime.strptime("01/01/19", '%d/%m/%y')
end_date = datetime.strptime("01/01/22", '%d/%m/%y')
start_time = st.slider("",
     min_value=start_date,
     max_value=end_date,
     format="DD/MM/YYYY"
)
