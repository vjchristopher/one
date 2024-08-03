import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.io as pio
import re
st.title('🔑Value of Spectrum acquired purely from auctions:')
st.markdown('''
            #### This :rainbow[does not] include:
            #####  :red[Administrative] spectrum,:blue[Liberalised] spectrum, :green[Shared] spectrum and :orange[Traded] spectrum. 
          
          ''')

#read in the file
#@st.cache_data

def load_holding_data():
    data_holding=pd.read_csv("spectrum_holding.csv")
    #st.dataframe(data)
    return data_holding

def load_value_data():
    data_value=pd.read_csv("valuation.csv")
    value_per_year=data_value.set_index('LSA').apply(lambda x: x/20)
    value_per_year=value_per_year.reset_index()
    #st.dataframe(value_per_year)
    return value_per_year

def load_acquistion_data():
    spectrum_acquired=pd.read_csv("tsp-lsa-band-all-auction.csv")
    #st.dataframe(data)
    return spectrum_acquired

def manage_acquistion_data():
    df=load_acquistion_data()
    df.band=df.band.astype('str') #convert to string
    df['acquired_year']=df['acquired_year'].apply(lambda x: str(x)) #convert to string
    df_pivot=df.pivot_table(index=['LSA','TSP','acquired_year'],columns='band',values=['bw','years_left']).fillna(0)
    df_pivot.columns = ['-'.join(col).strip() for col in df_pivot.columns.values] #flatten multi index
    return df_pivot


form_resource=st.form(key='Options')
form_resource.subheader('The market price for the spectrum held by different operators ')

#Just to get the LSA names
holding = load_holding_data()
#fill the NANS
holding.LSA=holding.LSA.fillna(method='ffill')
holding.iloc[:,2:]=holding.iloc[:,2:].fillna(0)# filling value 0 in NAN
#st.dataframe(holding)
#LSA List
lsa_list=holding['LSA'].unique().tolist() 
#Add 'ALL LSAs" to LSA List
lsa_list[:0]=['All LSAs']

#TSP List
tsp_list=holding['TSP'].unique().tolist() 

#Bandlist
band_list=holding.columns.unique().tolist()[2:] 

with form_resource: # Read the LSA, BANDS and TSPs
    LSAS= st.multiselect('Choose LSA:',options=lsa_list, default = ['All LSAs'])
    if 'All LSAs' in (LSAS):
        LSAS=lsa_list[1:] 
    BANDS=st.multiselect('Choose the Bands:',options=band_list, default = ['700 MHz band (paired)'])
    #st.write(BANDS)
    TSPS=st.selectbox('Choose the TSP',tsp_list)
    #st.write(TSPS)
    submitted_holding=st.form_submit_button(label='Assess the Value for the selected LSA ,TSP and BAND')



#After pressing the Button
if (submitted_holding):
    
    #Stage 1
    #Read Auction acquired data from the CSV file after processing it
    acquistion_data=manage_acquistion_data()
    acquistion_data=acquistion_data.reset_index()
    
    #Filter the data based on the Bands selected, the LSA selected and TSP selected.
    colums=["LSA"]
    for band in BANDS:  
        band=band.split()[0]        
        colums=colums+[col for col in acquistion_data if band in col]
    
    data=acquistion_data.query('LSA in @LSAS & TSP in @TSPS').loc[:,colums].reset_index(drop=True)
    #st.dataframe(data)
    #Remove all rows in which the values are all zeroes, which was created when the acquistion data was prepared using pivot table
    data=data.set_index('LSA')     
    data=data[~((data == 0).all(axis=1))]
    data=data.reset_index()
    
    #Stage 2 : create price matrix from the valuation file and price per year data for different auctions
    valuation=load_value_data()    
    BANDS = list(set(['LSA']+BANDS)) #only selecting the required bands
    pattern=[]
    for band in BANDS:
        pattern.append(band)
    #pattern='|'.join(BANDS) # this is not working in the streamlit     
    
    prices_matrix=valuation.filter(items=pattern)    
    
    #st.dataframe(prices_matrix)

    #Stage 3: merging the price file with the acquistion data based on common variable LSA    
    data_final=data.merge(prices_matrix,on='LSA')
    #st.dataframe(data_final)
    #remove duplicate columns
    data_final = data_final.loc[:,~data_final.columns.duplicated()].copy()
    
    #st.dataframe(data_final)
    data_final.to_csv('data_final.csv')

    #stage 4:  From the merged file separate out the relevant bands selected warlier using the item variable 
       
    data_final=data_final.set_index('LSA')
    
    BANDS.remove('LSA') #remove the LSA 
    
    #iterate over the bands (Now LSA is not in the BANDS)
    sum={}
    for item in BANDS:
        #st.write(item)
        item=item.split()[0]
        bw_col = data_final.filter(regex=f'bw-{item}$')        
        #st.dataframe(bw_col)
        
        yr_col = data_final.filter(regex=f'years_left-{item}$')
        #st.dataframe(yr_col)
        
        band_col = data_final.filter(regex=f'^{item}')
        #st.dataframe(band_col)
        
        #store_dict=dict([(item,[bw_col.iloc[:,0].sum(),yr_col.iloc[:,0].sum(),band_col.iloc[:,0].sum()])])
    # Compute the total and print it
        Total = bw_col.mul(yr_col.values, axis=1).mul(band_col.values, axis=1)
        #st.dataframe(Total)
        sum[item]=[bw_col.iloc[:,0].sum(),Total.iloc[:,0].sum()]
    # to store the prices in a row
    #st.write(sum) 
    st.subheader('Spectrum Acquired in the various Auctions and its current Market Price:', divider='rainbow')
   
    #convert the information n the Dictionary into a Dataframe
    Frame=pd.DataFrame(sum,index=['Holding in MHz','Price in Rs Crores'])
       
    Frame['Total']=Frame.sum(axis=1)
    Frame=Frame.T
    Frame = Frame.rename_axis('Bands', axis=0)
    #Frame.style.format(precision=2)  #rounding to two places   
    st.dataframe(Frame.style.format(precision=2))
    
   
    st.subheader('',divider='green') 
    st.subheader(f'Total Spectrum Acquired through different auctions by the TSP: {round(Frame.loc["Total","Holding in MHz"],2)} MHz' )
    st.subheader(f'Market price of the Spectrum held by the TSP: Rs {round(Frame.loc["Total","Price in Rs Crores"],2)} Crores' )
    st.subheader('',divider='green')