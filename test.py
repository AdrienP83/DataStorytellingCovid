import pandas as pd
import pandas_profiling
import streamlit as st

from streamlit_pandas_profiling import st_profile_report

##df = pd.read_csv("tousanticovid/tac_metriques.csv")
df = pd.read_csv("owid/owid-covid-data.csv")
pr = df.profile_report()

st_profile_report(pr)