import streamlit as st 
import pandas as pd

st.title('🔊Spectrum Holding of Different Telecom Operators in MHz:')

#read in the file
holding = pd.read_csv("spectrum_holding.csv")
valuation=pd.read_csv('valuation.csv')
#fill the NANS
holding.LSA=holding.LSA.fillna(method='ffill')
holding.iloc[:,2:]=holding.iloc[:,2:].fillna(0)# filling value 0 in NAN

valuation=valuation.set_index('service_area')

lsa_list=holding['LSA'].unique().tolist()
#Add 'ALL LSAs"
lsa_list[:0]=['All LSAs']
tsp_list=holding['TSP'].unique().tolist()
band_list=holding.columns.unique().tolist()[2:]


LSAS= st.multiselect('Choose LSA:',options=lsa_list, default = ['All LSAs'])
if 'All LSAs' in (LSAS):
    LSAS=lsa_list[1:] 
BANDS=st.multiselect('Choose the Bands:',options=band_list, default = ['700 MHz band (paired)'])
TSPS=st.selectbox('Choose the TSP',tsp_list)

#press the Button
if (st.button("Show the holding")):
    df=holding.loc[:,['LSA','TSP']+ BANDS]
    df=df.query('LSA in @LSAS & TSP in @TSPS').reset_index(drop=True)
    #st.dataframe(df)
    sum=0 # to store the prices in a row
    new_row=['Current Market Price',TSPS] #to store the column wise Total
    for i in range(len(BANDS)):
        for index, row in df.iterrows():
            sum+=row[BANDS[i]] * valuation.loc[row['LSA'],BANDS[i]]
            sum=round(sum,2)
        new_row.append(sum)
        sum=0        
    #To store the gross sum of all spectrum prices in the display 
    gross=0
    for fig in new_row[2:]:
        gross+=fig
    gross=round(gross,2)
    df.loc[len(df.index)]=new_row        
    df.set_index('LSA',inplace=True) 
    df.style.format(precision=2)  #rounding to two places   
    st.header('Quantum of Spectrum in MHz ', divider='rainbow')
    st.subheader('The last row in the table shows the indicative value for each spectrum bands in Rs.Crores as per the current Reserve Price.',divider='green')
    #st.subheader('bands in Rs.Crores as per the current Reserve Price.',divider='green')
    st.table(df.style.format(precision=2))
    st.subheader('',divider='green')
    col1, col2 = st.columns((14,2))
    with col1:
        st.subheader("Total Market Price of above spectrum in Rs.Cr: ")
    with col2:
        st.subheader(gross)
    st.subheader('',divider='green')
       