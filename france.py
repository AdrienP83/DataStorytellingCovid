import pandas as pd
import pandas_profiling
import streamlit as st
import numpy as np
from PIL import Image
from streamlit_pandas_profiling import st_profile_report


df = pd.read_csv("tousanticovid/tac_metriques.csv")

df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')
df1 = df[df['date'] >= pd.to_datetime('2020-01-01', format = '%Y/%m/%d')]
df1 = df1.sort_values('date', ascending = True)
## code
st.markdown("# Page France 🇫🇷")
st.sidebar.markdown("# Page France 🇫🇷")



##vaccine_state = pd.DataFrame.from_records(results2)
##vaccine_state = vaccine_state.sort_values(by='date')
pr = df1.profile_report()
st_profile_report(pr)
st.markdown("***")
st.markdown("### 9 nov. 2020")
image = Image.open('tousanticovid/img1.png')
st.image(image, caption='Mise en graphique pour voir la dynamique et comparaison avec le nombre de cas positif confirmés quotidiens.')
st.markdown("***")
image = Image.open('tousanticovid/gestes.png')
st.image(image, caption='Ensemble contre le Covid-19')
st.markdown("***")
image = Image.open('tousanticovid/app.png')
st.image(image, caption='Arrivée de Tous AntiCovid en Juin 2020')