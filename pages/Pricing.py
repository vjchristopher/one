import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt

#st.title("Pricing.")

from PIL import Image

#import json

#---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit

#---------------------------------#
# Title

st.markdown("***Best Viewed on Laptops and Desktops***.")

# image = Image.open('auction.jpg')

# col1,col2,col3=st.columns(3)
# with col2:
#     st.image(image,width=200) 
st.header('💲Reserve Price and Winning Price in various auctions in tabular and graphic form - Press "Submit" button in the Sidebar Panel:')
# st.markdown("""
# 💾  
# -------------------------------------------            
# """)


#initialise
service_area_list=['All LSAs','AP','Assam','Bihar','Delhi','Gujarat','Haryana','HP','J & K','Karnataka','Kerala','Kolkata',
                   'MP','Maharashtra','Mumbai','NE','Odisha','Punjab','Rajasthan','TN','UP(E)','UP(W)','WB'] 
auction_year_list=['All Auctions',2010,2012,2013,2014,2015,2016,2021,2022,2024]
freq_bands_list=['All Bands','600','700','800','900','1800','2100','2300','2500','3300 MHz','26 GHz']


#---------------------------------#
# Sidebar + Main panel
form1=st.sidebar.form(key='Options')
form1.header('Selection Panel')
#image = Image.open('auction.jpg')
#form1.image(image, width = 120) 
#form1.form_submit_button(label='Submit')
with form1:
    service_area= form1.selectbox('Select the service area',service_area_list,key='key1')
    auction_year = form1.selectbox('Select auction year',auction_year_list,key='key2')
    freq_bands=form1.selectbox('Select frequency bands',freq_bands_list,key='key3')
    submitted = st.form_submit_button(label='Submit')
#-----------------------------------#
#plotly template fixing#
pio.templates.default = "plotly"
pd.options.plotting.backend = "plotly"
#-----------------------------------#


@st.cache_data

def load_data():
    df=pd.read_csv(r'combined_file_RP_WP_cols_ordered.csv')
    #st.dataframe(df)
    return df
  
def read_lsa():
    lsa= service_area
    return lsa

def read_auction_year():
    year=auction_year
    return year

def read_bands():
    bands=freq_bands
    return bands

def process_df(df):  
    df=df.set_index('service_area')      
    df=df.apply(pd.to_numeric)
    #st.dataframe(df)
    return(df)
  
def write_text(txt):
    st.write(txt)
  
def plot_df(data):
     fig1=px.line(data,markers=True,line_shape=None,template=None,title='Reserve Price and Winning Price in auctions')
     fig1.update_layout(
        #width=1600,
        #height=600,
     title_text='Reserve Price-Winning Price comparison in Different Auctions<br><br>WPC.\\2024'    
     )
     st.plotly_chart(fig1)

     fig2=px.scatter(data,template='plotly_dark',title='Reserve Price and Winning Price in auctions')
     #fig2.update_traces(marker_line_color='black', marker_line_width=1)
     fig2.update_layout(
     #width=1600,
     #height=600,
     title_text='Reserve Price-Winning Price comparison in Different Auctions<br><br>WPC.\\2024',
     plot_bgcolor="#262730" # for streamlit to have the dark background
     )
     st.plotly_chart(fig2)   
#main() , initialise the data, process and plot. 
#Capture the data in the select boxes

df=load_data()
df=process_df(df)

if submitted: #The submit button has been pressed.  
    lsa=read_lsa()
    year=read_auction_year()
    band=read_bands()
    
    # st.dataframe(df.filter(like='_'+str(band), axis=1))
    if lsa=='All LSAs':
        #st.dataframe(df)
        lsa=service_area_list[1:]                        
    if year=='All Auctions':
        year=df.columns # all columns        
    else:
        year=[col for col in df.columns if str(year) in col]        
    if band=='All Bands':
        fbands=df.columns # all columns
    else:        
        fbands=[col for col in df.columns if ( '_'+str(band)) in col]
        
    #st.dataframe(df.filter(like='_'+str(year), axis=1).filter(like='_'+str(band), axis=1))    
    #devlop the dataframes according to the selection in two stages:
    # one with the LSA and year selection and the other     
    #with LSA and band selection
   
    df2=df.loc[lsa,year]
    if not isinstance(df2, pd.DataFrame):
        df2=pd.DataFrame(df2).T
    #st.dataframe(df2.T) # year selected  
    #plot_df(df2) 
    # now in the dataframe filter those belonging to the band if any selected
    new_columns_list=[]
    for fband in fbands:
        if fband in df2.columns:
            new_columns_list.append(fband)
    #st.write(new_columns_list)
    df3=df2.loc[:,new_columns_list]
    
    st.subheader('"0" indicates no spectrum available in that LSA',divider='blue') 
    st.subheader('"-1" indicates none was taken though spectrum was available',divider='blue')
    
    st.dataframe(df3)
    #write the footnotes of explanantion
    txt_out2='1.Spectrum Prices are all in Rs. Crores and it is per Block.'
    txt_out3='2.The Block Size differs from auction to auction.'
    txt_out4='3.The nomenclature-1: RP_2100_2010: Reserve Price for 2100 MHz in the 2010 Auction'
    txt_out5='4.The nomenclature-2: WP_26_2022: Winning Price for 26 GHz in the 2022 Auction'
    txt_out6='1.The Charts are plotted after the Block sizes are normalised for same freq bands from different auctions'
    write_text(txt_out2)
    write_text(txt_out3)
    write_text(txt_out4)
    write_text(txt_out5) 
    st.subheader('',divider='blue')
    #plot the charts
    plot_df(df3) 
    #footnote to the chart
    write_text(txt_out6)    
    
#st.write("Outside the form")


