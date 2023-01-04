import pandas as pd
import pandas_profiling
import streamlit as st
import numpy as np
from PIL import Image
from streamlit_pandas_profiling import st_profile_report

df = pd.read_csv("owid/dataset_covid_world.csv")

## code
st.markdown("# Page France 🇫🇷")
st.sidebar.markdown("# Page France 🇫🇷")

st.markdown("### 9 nov. 2020")
image = Image.open('tousanticovid/img1.png')

st.image(image, caption='Mise en graphique pour voir la dynamique et comparaison avec le nombre de cas positif confirmés quotidiens.')

pr = df.profile_report()

st_profile_report(pr)