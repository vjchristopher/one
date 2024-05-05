import streamlit as st 
import pandas as pd

st.icons("table")
st.header('Different Band plans used by the Telecom Operators in India:', divider='blue')

band_names=pd.read_csv("band_names.csv")
band_names.index += 1
st.table(band_names)

