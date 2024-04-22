import streamlit as st
import pandas as pd
import plotly.express as px

# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#local_css("style.css")

st.title('Spectrum Sharing and Trading Information:')
#read in the file
share= pd.read_csv("share.csv")
trade=pd.read_csv("trade.csv")

#st.dataframe(valuation)
share.band=share.band.fillna(method='ffill') #LSA filling with previous value in place of NAN
share.tsp1=share.tsp1.fillna(method='ffill')
share.tsp2=share.tsp2.fillna(method='ffill')
#st.write(share.query('tsp1=="RCL"'))
trade.band=trade.band.fillna(method='ffill') #LSA filling with previous value in place of NAN
trade.seller=trade.seller.fillna(method='ffill')
trade.buyer=trade.buyer.fillna(method='ffill')

#first strip the blank spaces
share['lsa']=share['lsa'].str.strip()
trade['lsa']=trade['lsa'].str.strip()

lsa_share=share['lsa'].unique().tolist()
lsa_trade=trade['lsa'].unique().tolist()
tsp_list1=share['tsp1'].unique().tolist()
tsp_list2=share['tsp2'].unique().tolist()

sellers=trade['seller'].unique().tolist()
buyers=trade['buyer'].unique().tolist()
# tsp_list=holding['TSP'].unique().tolist()
band_sharing=[800,1800,2100]
band_trading=[800,1800,2300]

#st.write(lsa_list)    

#create a multiselect widget to display genre
share_tab,trade_tab=st.tabs(['Spectrum Share','Spectrum Trade'])
with share_tab:
    BANDS=st.multiselect('Choose the Bands:',options=band_sharing, default = [800,])
    LSAS= st.multiselect('Choose LSA:',options=lsa_share, default = ['Andhra Pradesh',])
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

with trade_tab:
    BANDS=st.multiselect('Choose the Bands:',options=band_trading, default = [800,])
    LSAS= st.multiselect('Choose LSA:',options=lsa_trade, default = ['Andhra Pradesh',])
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
        
           
        
