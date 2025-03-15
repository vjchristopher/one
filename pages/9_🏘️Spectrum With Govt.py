import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
np.set_printoptions(legacy='1.25')
st.set_page_config(layout="wide",page_title = "This is a Multipage WebApp") 
st.title('🧳Spectrum Reserve:')
#st.subheader('Updated Post Auction 24')

#read in the file
#@st.cache_data

def load_data():
    data=pd.read_csv("spectrum_available.csv")
    #st.dataframe(data)
    return data
# 2. Now the holding table part


gov_holding = load_data()

valuation=pd.read_csv('value_reserve_spectrum.csv')
#fill the NANS
gov_holding.LSA=gov_holding.LSA.fillna(method='ffill')
gov_holding.iloc[:,2:]=gov_holding.iloc[:,2:].fillna(0)# filling value 0 in NAN

#valuation=valuation.set_index('LSA')
#st.dataframe(valuation)
lsa_list=gov_holding['LSA'].unique().tolist()
#Add 'ALL LSAs"
lsa_list[:0]=['All LSAs']
#tsp_list=holding['TSP'].unique().tolist()
band_list=gov_holding.columns.unique().tolist()[1:]
#st.write(band_list)
form_holding=st.form(key='Options1')
form_holding.subheader('The info on Spectrum left with the Govt and its value as per last auction price: ')

with form_holding:
    
    LSAS= st.multiselect('Choose LSA:',options=lsa_list, default = ['All LSAs'])
    
    if 'All LSAs' in (LSAS):
        LSAS=lsa_list[1:] 
    BANDS=st.multiselect('Choose the Bands:',options=band_list, default = band_list[0])
    submitted=st.form_submit_button(label='Submit')
  
#press the Button
if (submitted):
    
    st.markdown('''
            #### The following table has the Band column followed by the respective Price column:
            #####  :red[1.] Spectrum available with the Government in the selected LSA and Band \n\
            #####  :orange[2.] The value of the Spectrum as per the Price fixed/found in 2024 Auction. 
          
          ''')
    st.subheader('',divider='blue')
    df1=gov_holding.loc[:,['LSA']+ BANDS]
   
    df1=df1.query('LSA in @LSAS').reset_index(drop=True)
    df1=df1.set_index('LSA')
    
    # Identify numeric columns only
    numeric_cols = df1.select_dtypes(include='number').columns
    
    # Calculate column-wise totals for numeric columns
    totals = df1[numeric_cols].sum()

    # Add a new row with totals for numeric columns; others set as empty or custom value
    df1.loc['Total'] = [totals.get(col, '') for col in df1.columns]
    
    #round the figure to 2 decimal places
    df1=df1.round(2)
    
    #df1.loc['Total']=df1.sum()
    #st.dataframe(df1)   
    df2=valuation.loc[:,['LSA']+ BANDS]
    df2=df2.query('LSA in @LSAS').reset_index(drop=True)
    df2=df2.set_index('LSA')
    # Identify numeric columns only
    numeric_cols = df2.select_dtypes(include='number').columns
    # Calculate column-wise totals for numeric columns
    totals = df2[numeric_cols].sum()
    # Add a new row with totals for numeric columns; others set as empty or custom value
    df2.loc['Total'] = [totals.get(col, '') for col in df2.columns]
    #df2 = df2.add_suffix('_price_in_₹_Crores')
    #st.dataframe(df2)

    #multiply the bands with price
    price_info=df1*df2

    #st.dataframe(price_info)              

    #add a Total new row
    price_info.loc['Total']=price_info.sum()

    #round the figure to 2 decimal places
    price_info=price_info.round(2)

    #add a suffix to the price to distinguish from the Band columnnames
    price_info=price_info.add_suffix('_price_in_₹_Crores')

    #now merge the band and price info dataframes
    merged_df = pd.concat([df1, price_info], axis=1)
        
    # Your desired column order (if present)    
    preferred_order = ['600 MHz','600 MHz_price_in_₹_Crores','700 MHz','700 MHz_price_in_₹_Crores',	
                       '800 MHz','800 MHz_price_in_₹_Crores','900 MHz','900 MHz_price_in_₹_Crores',
                       '1800 MHz','1800 MHz_price_in_₹_Crores','2100 MHz','2100 MHz_price_in_₹_Crores',
                       '2300 MHz','2300 MHz_price_in_₹_Crores','2500 MHz','2500 MHz_price_in_₹_Crores',
                       '3300 MHz','3300 MHz_price_in_₹_Crores','26 GHz','26 GHz_price_in_₹_Crores']
    
    
    #Filter the preferred columns that actually exist in the DataFrame
    existing_preferred = [col for col in preferred_order if col in merged_df.columns]

    #Formulate the dataframe as per the seclection of LSA and Bands
    merged_df=merged_df[existing_preferred]

    # Define which columns are quantity and which are price
    quantity_cols = [col for col in existing_preferred if col.endswith('MHz')]
    price_cols = [col for col in existing_preferred if col.endswith('_Crores')]

    # Replace 0s in quantity columns with 'X'
    merged_df[quantity_cols] = merged_df[quantity_cols].mask(merged_df[quantity_cols] == 0, 'X')
    # Replace 0s in price columns with 'Y'
    merged_df[price_cols] = merged_df[price_cols].mask(merged_df[price_cols] == 0, 'Y')
    
    # #Replace all 0s in the DataFrame with 'X'
    # merged_df = merged_df.mask(merged_df == 0, 'X')

    st.dataframe(merged_df)   
    
    st.subheader('',divider='blue')
    st.markdown('''
                ##### The 'X' in the band columns indicate that no spectrum is available in that LSA.
                ##### The 'Y' in the price columns indicates that it was not sold in the 2024 auction in that LSA.
                ''')
   
    
   
   