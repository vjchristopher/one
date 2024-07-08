
import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly
import matplotlib.pyplot as plt
pd.options.plotting.backend='plotly'
#plotting RP and SP for different auctions using slopegraph



st.subheader('Reserve Price and Selling Price (Winning Price) compared in various auctions :')

auction_year_list=[2010,2012,2013,2014,2015,2016,2021,2022,2024]
freq_bands_list=['600','700','800','900','1800','2100','2300','2500','3300','26']


#---------------------------------#
# Sidebar + Main panel
form1=st.sidebar.form(key='Options')
form1.header('Selection Panel for comparing RP and SP')
with form1:    
    auction_year = form1.selectbox('Select auction year',auction_year_list,key='key1')
    freq_bands=form1.selectbox('Select frequency bands',freq_bands_list,key='key2')
    submitted = st.form_submit_button(label='Submit')
#-----------------------------------#
#functions

@st.cache_data

def load_data():
    df=pd.read_csv(r'combined_file_RP_WP_cols_ordered.csv')
    return df
 
def read_auction_year():
    year=auction_year
    return year

def read_bands():
    bands=freq_bands
    return bands

def process_df(df):  
    df=df.set_index('service_area')      
    df=df.apply(pd.to_numeric)
    return(df)
  
#find duplicate values in the reserve price and selling price and accordingly return two dictionaries with the service areas
#that has the same price and bunched together to enable to indicate in the slopegraph plot.
def find_repeated_rp(df):
    column_rp=df.columns[0]
    column_sp=df.columns[1]
    #for RP
    
    repeat_list_rp=df.loc[df[column_rp].duplicated(),:][column_rp].to_list() #find duplicated reserve prices first  
    repeat_list_rp = list(set(repeat_list_rp)) #to remove duplicates from the list itself
    duplicate_rp=dict.fromkeys(repeat_list_rp, []) #create a dictionary first
    #print(duplicate_rp)
    #for sP
    repeat_list_sp=df.loc[df[column_sp].duplicated(),:][column_sp].to_list() #find duplicated reserve prices first  
    repeat_list_sp = list(set(repeat_list_sp)) #to remove duplicates from the list itself
    duplicate_sp=dict.fromkeys(repeat_list_sp, []) #create a dictionary first
    #print(duplicate_sp)
    list1=[]
    for x in repeat_list_rp:
        for index, row in df.iterrows():        
            if (row[column_rp]==x):            
                list1.append(index)
        #transfer the list to  dictionary duplicate
        duplicate_rp[x]=list1
        list1=[] #reset the list for next iteration
    #for SP
    list2=[]
    for y in repeat_list_sp:
        for index, row in df.iterrows():        
            if (row[column_sp]==y):            
                list2.append(index)
        #transfer the list to  dictionary duplicate
        duplicate_sp[y]=list2
        list2=[] #reset the list for next iteration
    return duplicate_rp,duplicate_sp

# set the parameters for plotting the slope graph. Major thing is the annotations at the Reserve price and the Selling price ends.
# 

def plot_slope(df):
    
    #duplicate LSA s in reserve price columns of the dataframe
    if df.empty:
        #st.write("Dataframe empty")
        return
    #first find the LSA s with the same Reserve Price and same selling price in two dictionaries
    dup_rp,dup_sp=find_repeated_rp(df)
    #st.write(dup_rp,dup_sp)    
    df=df.T
    fig=df.plot(markers=True)
    fig.update_traces(marker_size=12)
    fig.update_layout(
    {'plot_bgcolor':'ivory'},
    showlegend=False,
    #title='Reserve Price vs Selling Price in various auctions using sloppegraph',
    #xaxis={'title':''},
    yaxis={'visible':True},
    )

    for data,col in zip(fig.data,df.columns):    
        # col is divided into colx and coly representations for x and y because x, y in single pass ( for x, y in enu....]
        # copy the same col to y wrogly if we use the same name col in both x==0 and x!=0 logic
       
        data.x=['Reserve Price','Selling Price']
        for x,y in enumerate(df[col]): # x=0, y=RP; x=1,y=SP          
            #st.write(x,y) 
            if x==0: #x=0 corresponding to RP
                if (y in dup_rp.keys()):
                    colx=dup_rp[y] #to factor the multiple LSA s with the same reserve price
                else:
                    colx=col
                fig.add_annotation(x=x,y=y,text=f'Rs {y} Crores <br>{colx} ',showarrow=False,
                                  width=200,align='right',
                                  xshift=-110,
                                  yshift=0,
                                  #font={'color':color}
                                  )
                
            else: # x=1 corresponding to SP
                # st.write("x=",x)
                # st.write(col)
                if (y in dup_sp.keys()):
                    coly=dup_sp[y] #to factor the multiple LSA s with the same selling price
                else:
                    coly=col
                if y==-1:
                    #split if columns more than 4
                    
                    coly1 = coly[:len(coly)//2]
                    coly2 = coly[len(coly)//2:]
                    fig.add_annotation(x=x,y=0,text=f' No Bids recevd for LSAs in <br>{coly1} and<br>{coly2} ',showarrow=False,
                                  width=300,align='left',
                                  xshift=150,
                                  yshift=0,
                                  #xanchor="left"
                                  #font={'color':color}
                                  )   

                else:                    
                    fig.add_annotation(x=x,y=y,text=f' Rs {y} Crores <br>{coly} ',showarrow=False,
                                  width=200,align='left',
                                  xshift=110,
                                  yshift=0,
                                  #xanchor="left"
                                  #font={'color':color}
                                  )           
    #fig.update_xaxes=range([-.2,1.2])
    #fig.add_trace()
    fig.update_layout(
    autosize=True,
    width=1000,
    height=800,
    #hovermode="y unified"
    xaxis=dict(tickfont=dict(size=20, color='black')),
    #yaxis=dict(tickfont=dict(size=20, color='black')),
    yaxis_title="Price in Rs. Crores",
    xaxis_title=""
    )
    st.plotly_chart(fig)
    return(fig)
# main
df=load_data()
df=process_df(df)
#st.dataframe(df)
if submitted: #The submit button has been pressed.  
    year=read_auction_year() 
    band=read_bands()
    st.markdown(f"Sub: Frequency band {band}  MHz Bid outcome from  {year}  auction.")

    #st.write(band)   
    # st.write(year)
    # st.write(band)    
    #df1=df.filter(regex='(?=.*{year})(?=.*{band})') 
    df1=df.filter(regex=(f'(?=.*{year})(?=.*{band})')) 
    #remove all zero values in the reserve price
    if band=='800': # because when 800 is selected, 1800 also joins.
        #st.write('checking')
        df1=df.filter(regex=(f'(?=.*{year})(?=.*_{band})')) 
    if df1.empty:
        st.write('No data available for the combination selected')
    else:
        df1=df1[df1.iloc[:,0]!=0]
    #call the plot function
    #st.dataframe(df1)
    
    (df1.pipe(plot_slope))  
    st.subheader(" :orange[A negative value (-1) for the Selling Price in any LSA, if any\
                  indicates no offers were received for the selected band in that LSA.]")
