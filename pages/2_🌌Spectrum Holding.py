import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.io as pio

st.title('🔊Spectrum Holding as Pie Chart and in Tabular form:')

#read in the file
#@st.cache_data

def load_data():
    data=pd.read_csv("spectrum_holding.csv")
    #st.dataframe(data)
    return data

def show_pie_chart(band):
    #st.write(band)
    df=load_data()    
    df=df.fillna(0).drop(columns='LSA')
    df1=df.groupby('TSP',as_index=False).sum()
    col=df1.columns[1:].to_list()
    df1['Total']=df1[col].sum(axis=1)
    #the band number
    #band=band_dict[no]
    if band=="All Spectrum Bands":
        fig = px.pie(df1, values='Total', names='TSP',title=f"Distribution of {band} among the operators",
                    labels={'Total':'Total spectrum in MHz'},
                    color_discrete_sequence=px.colors.qualitative.Dark24,hole=0.6)
    else:
        fig =px.pie(df1, values=band, names='TSP',title=f"Distribution of {band} among the operators",labels={band:'Bandwise spectrum in MHz'},
                    color_discrete_sequence=px.colors.qualitative.Vivid,hole=0.6)
        
    fig.update_traces(texttemplate='%{label}: %{value}', textposition="outside")
    fig.update_layout(
    width=800,
    height=800,
    font_family='Segoe UI',
    font_size=15
    )    
    st.plotly_chart(fig)     
    return 
#1. pie chart part

band_dict={0:'700 MHz band (paired)',
         1:'800 MHz band (paired)',         
         2:'900 MHz band (paired)',
         3:'1800 MHz band (paired)',
         4:'2100 MHz band (paired)',
         5:'2300 MHz band (unpaired)',
         6:'2500 MHz band (unpaired)',
         7:'3300 MHz band (unpaired)',
         8:'26 GHz band (unpaired)', 
         9:'All Spectrum Bands'        
         }

form_pie=st.form(key='Options')
form_pie.subheader('The distribution of different bands shared among the TSP')
cols = form_pie.columns(10)


with form_pie:
    for i in range(10):
        with cols[i]:            
            st.checkbox(f'{band_dict[i]}',key=f"cb{i}") #define the checkboxes
    submitted=st.form_submit_button(label='Submit')
    if submitted:
        for i in range(10):            
            if st.session_state[f"cb{i}"] == True: #checking if any checkbox is pressed                  
                #st.markdown(f'this is {band_dict[i]}')
                show_pie_chart(band_dict[i])


  
# 2. Now the holding table part

form_holding=st.form(key='Options2')
form_holding.subheader('The holding of different spectrum bands among the TSP s and the value as per market price ')

holding = load_data()

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

with form_holding:
    LSAS= st.multiselect('Choose LSA:',options=lsa_list, default = ['All LSAs'])
    if 'All LSAs' in (LSAS):
        LSAS=lsa_list[1:] 
    BANDS=st.multiselect('Choose the Bands:',options=band_list, default = ['700 MHz band (paired)'])
    TSPS=st.selectbox('Choose the TSP',tsp_list)
    submitted_holding=st.form_submit_button(label='Show the holding')
#dictionaries for the selection

#press the Button
if (submitted_holding):
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
    #st.subheader('The last row in the table shows the indicative value for each spectrum bands in Rs.Crores as per the current Reserve Price.',divider='green')
    #st.subheader('bands in Rs.Crores as per the current Reserve Price.',divider='green')
    st.dataframe(df.style.format(precision=2))
    st.subheader('',divider='green')
    # col1, col2 = st.columns((14,2))
    # with col1:
    #     st.subheader("Total Market Price of above spectrum in Rs.Cr: ")
    # with col2:
    #     st.subheader(gross)
    # st.subheader('',divider='green')
       