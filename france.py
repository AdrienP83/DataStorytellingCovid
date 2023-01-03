import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

df = pd.read_csv("tousanticovid/tac_metriques.csv")
df_vacc = pd.read_csv("tousanticovid/France.csv")
df.columns

## code
st.markdown("# Page France 🇫🇷")
st.sidebar.markdown("# Page France 🇫🇷")

st.markdown("### 9 nov. 2020")
image = Image.open('tousanticovid/img1.png')

st.image(image, caption='Mise en graphique pour voir la dynamique et comparaison avec le nombre de cas positif confirmés quotidiens.')