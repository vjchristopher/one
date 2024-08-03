import streamlit as st 
import pandas as pd
import plotly.express as px


st.title('🤝🏻Spectrum Sharing Information:')
#read in the file
share= pd.read_csv("share.csv")

share.band=share.band.fillna(method='ffill') #LSA filling with previous value in place of NAN
share.tsp1=share.tsp1.fillna(method='ffill')
share.tsp2=share.tsp2.fillna(method='ffill')

#first strip the blank spaces
share['lsa']=share['lsa'].str.strip()


lsa_share=share['lsa'].unique().tolist()
#append the ALL LSAs
lsa_share[:0]=['All LSAs']
tsp_list1=share['tsp1'].unique().tolist()
tsp_list2=share['tsp2'].unique().tolist()

band_sharing=[800,1800,2100]


BANDS=st.multiselect('Choose the Bands:',options=band_sharing, default = [800,])
LSAS= st.multiselect('Choose LSA:',options=lsa_share, default = ['All LSAs',])
#If 'All LSAs selected:
if 'All LSAs' in (LSAS):
    LSAS=lsa_share[1:] 
TSPS1=st.selectbox('Choose the first TSP sharing spectrum',tsp_list1)
TSPS2=st.selectbox('Choose the second TSP sharing spectrum',tsp_list2)

if (st.button("Sharing Info")):        
    df=pd.DataFrame()       
    df=share[((share['tsp1']==TSPS1) & (share['tsp2']==TSPS2) & (share['band'].isin(BANDS)) & (share['lsa'].isin(LSAS)))]
    if not(df.empty):
        st.header(f"Sharing spectrum between {TSPS1} and {TSPS2}")
        st.write(df.reset_index(drop=True))
    else:
        st.header(f"No Sharing between {TSPS1} and {TSPS2} w.r.t selection above")
    #plot the spectrum shared
    chart_data_share=df[['lsa','bw_tsp1','bw_tsp2']]
    st.bar_chart(chart_data_share,x='lsa',y=['bw_tsp1','bw_tsp2'],color=["#FF0000", "#0000FF"],height=400)


        
