import streamlit as st 
import pandas as pd

st.header('🔊 Different Band plans used by the Telecom Operators in India:', divider='Blue')

band_names=pd.read_csv("band_names.csv")
st.table(band_names)

