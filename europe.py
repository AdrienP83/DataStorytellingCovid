import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv("owid/owid-covid-data.csv")
df.columns

## code
st.markdown("# Page Europe 🇪🇺")
st.sidebar.markdown("# Page Europe 🇪🇺")

st.markdown("### Évolution des différents aspects du Covid-19 en Europe")
df = pd.DataFrame(
    np.random.randn(0, 2) / [500, 500] + [43.509576948063675, 5.421613454818726],
    columns=['lat', 'lon'])

st.map(df)