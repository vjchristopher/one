import streamlit as st 
import pandas as pd
import plotly.express as px


st.title('💰Spectrum Trading Information:')
#read in the file
#share= pd.read_csv("share.csv")
trade=pd.read_csv("trade.csv")

trade.band=trade.band.fillna(method='ffill') #LSA filling with previous value in place of NAN
trade.seller=trade.seller.fillna(method='ffill')
trade.buyer=trade.buyer.fillna(method='ffill')

trade['lsa']=trade['lsa'].str.strip()


lsa_trade=trade['lsa'].unique().tolist()
#append the ALL LSAs
lsa_trade[:0]=['All LSAs']

sellers=trade['seller'].unique().tolist()
buyers=trade['buyer'].unique().tolist()
band_trading=[800,1800,2300]


BANDS=st.multiselect('Choose the Bands:',options=band_trading, default = [800,])
LSAS= st.multiselect('Choose LSA:',options=lsa_trade, default = ['Andhra Pradesh',])
#If 'All LSAs selected:
if 'All LSAs' in (LSAS):
    LSAS=LSAS[1:] 
SELLER=st.selectbox('Choose the Seller of spectrum',sellers)
BUYER=st.selectbox('Choose the Buyer of spectrum',buyers)

if (st.button("Trading Info")):
    df=pd.DataFrame()       
    df=trade[((trade['seller']==SELLER) & (trade['buyer']==BUYER) & (trade['band'].isin(BANDS)) & (trade['lsa'].isin(LSAS)))]
    if not(df.empty):
        st.header(f"Trading spectrum between {SELLER} and {BUYER}",divider='green')
        
        st.write(df.reset_index(drop=True))
        #st.write(df.dtypes)
        sum=round(df['traded_price'].sum(),2)
        st.subheader(f'The transaction amount is in Rs.Crores : {sum}',divider='green')
    else:
        st.header(f"No Trading between {SELLER} and {BUYER} w.r.t selection above",divider='green')
    #plot the spectrum traded using plotly express    
    chart_data_trade=df[['lsa','traded_spectrum','traded_price']]

    fig=px.bar(chart_data_trade,x='lsa',y=['traded_spectrum','traded_price'],barmode='group',
                text_auto = True,title='Spectrum traded in MHz and its price in Rs.Crores',
                labels = {'lsa': 'LSA', 'value': 'spectrum/price'})
    
    fig.update_traces(textfont_size = 14, textangle = 0, textposition = "outside") #to make the texts tight

    st.plotly_chart(fig)
    
        
    
