
import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly
import matplotlib.pyplot as plt
pd.options.plotting.backend='plotly'
#plotting RP and SP for different auctions using slopegraph
st.set_page_config(page_title="Charting It",
                   page_icon="",
                   layout="wide")
st.markdown("***Best Viewed on Laptops and Desktops***.")
st.header('🆚 Activity plots for the various auctions :', divider='grey')


def preprocess(frame):
   #st.table(frame.head())
   frame=frame.query('prov_win_bid!="-" ')\
        .query('prov_rank!="-"')\
        .query('bid_decision=="Bid"')\
        .reset_index()
   return frame

def pivot_data(frame):
   table = pd.pivot_table(frame, values=['prov_rank','prov_win_bid'], index=['Clock_Round','Service_Area'],
                       columns=['Bidder'], aggfunc="min")
   table.columns.name=''
   table=table.reset_index()
   table=table.fillna(0) 
   table.columns=['_'.join(col).strip() for col in table.columns.values]  
   return table

def read_blocks(auct_year,auct_band):
    block_df=pd.read_csv('all_blocks.csv')
    # from the column name find out the corresponding data   
    col_name=str(auct_year)+'-'+str(auct_band)
    if (col_name) in block_df.columns:
        return block_df.loc[:,['LSA',col_name]]
    

#function to plot the line graph
def plotly_plot(frame,lsa,type,blk):
       
    st.subheader(f' No of Blocks Auctioned in this service area= {blk}')

    colums=frame.columns 
    #Define the title of the plots
    max_clocks=frame.Clock_Round.max()
    if type=='Bid Value':
        title=f'The progress of the Bids in {max_clocks} clock rounds with the change in the Bid Values for LSA: {lsa}'
        #text_auto='0.02f'
    else:
        title=f'The progress of the Bids {max_clocks} clock rounds with the change in the Bid Ranks for LSA: {lsa}'
        #text_auto='auto'
    
    fig=(frame.plot(kind='scatter',x='Clock_Round',y=colums[2:],
                 title=title,
                 labels={'value':type}))
    if type=='Bid Rank':
        fig.update_yaxes(range=[-1,5])    
    fig.update_traces(marker=dict(size=20,
                              line=dict(width=1,
                              color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig.update_traces(mode='lines+markers+text',
                  textposition='top center')
    fig.update_layout(
    title=dict(text=title, font=dict(size=20), automargin=False, yref='paper'),
    #margin={'t':100},
    yaxis={'title':'Bid Prices'},
    #coloraxis_colorbar={'title':type}, 
    legend_title_text='Bidders',
    )
    fig.update_yaxes(tickfont_size=20, ticks="outside", ticklen=5, tickwidth=3)
    fig.update_xaxes(tickfont_size=20,tickangle=0,side='bottom')    
    st.plotly_chart(fig)    
    return #fig


#function to plot the heatmap
def plotly_imshow(frame,lsa,type,blk):
    colums=frame.columns    
    st.subheader(f' No of Blocks Auctioned in this service area= {blk}')  
    
    frame=frame.drop(columns='Service_Area')
    max_clocks=frame.Clock_Round.max()
    frame=frame.set_index('Clock_Round')
    
    #Define the title of the plots
    if type=='Bid Value':
        title=f'The progress of the Bids in {max_clocks} clock rounds with the change in the Bid Values for LSA: {lsa}'
        text_auto='0.02f'
    else:
        title=f'The progress of the Bids in {max_clocks} clock rounds with the change in the Bid Ranks for LSA: {lsa} '
        text_auto='auto'
    fig=px.imshow(frame,width=1400,height=800,color_continuous_scale='RdBu_r',                                       
                  text_auto=text_auto,aspect='auto')
    fig.update_layout({
    'paper_bgcolor':'white',
    'font_color':'black', 
    'font_size':20,
    
    },
    title=dict(text=title, font=dict(size=20), automargin=False, yref='paper'),
    margin={'t':150},
    yaxis={'title':''},
    coloraxis_colorbar={'title':type},      
    )  
    
    fig.update_yaxes(tickfont_size=20, ticks="outside", ticklen=5, tickwidth=3)
    fig.update_xaxes(tickfont_size=20,tickangle=0,side='top')
    
    st.plotly_chart(fig)
    return #fig

#dictionaries for the selection
my_dict={2010:[2100,2300],
         2012:[1800],         
         2014: [900,1800],
         2015:[800,900,1800,2100],
         2016: [800,1800,2100,2300,2500],
         2021: [800,900,1800,2100,2300],
         2022: [700,800,900,1800,2100,2500,3300,26],
         }

my_dataframe={2010: ['Auction2010_3G_Bid_Trail_Data.csv','Auction2010_BWA_Bid_Trail_Data.csv'],
              2012:'Auction2012_Bid_Trail_Data.csv',
              2014:'Auction2014_Bid_Trail_Data.csv',
              2015:'Auction2015_Bid_Trail_Data.csv',
              2016:'Auction2016_Bid_Trail_Data.csv',
              2021:'Auction2021_Bid_Trail_Data.csv',
              2022:'Auction2022_Bid_Trail_Data.csv'}

#First write the Spectrum Auction SMRA type

col1, col3 = st.columns([2,2])
with col1:
  auction_year = st.selectbox('Choose the auction year', options=(v for v in my_dict.keys()), 
                               key=1)
with col3:
  auction_band = st.selectbox('Choose the frequency band ', options=my_dict[auction_year], key=2)

#st.write("you selected ",auction_band)
st.divider()
#Read the dataframe on the basis of the year selected:
if ( auction_year==2010 and auction_band==2100):
   csv=my_dataframe[auction_year][0]
elif ( auction_year==2010 and auction_band==2300):
   csv=my_dataframe[auction_year][1]
else:
   csv=my_dataframe[auction_year]
#st.write(csv)
df=pd.read_csv(csv,index_col=0)

if 'Band' in df.columns:
   df=df.query('Band==@auction_band')
df=preprocess(df)

table=pivot_data(df)


# Select the LSA
lsa_names=table['Service_Area_'].unique().tolist()

#Creates two frames for two types of display. First create the columns required
winrank_columns=['Clock_Round_','Service_Area_']+[col for col in table.columns if 'rank' in col]
winbid_columns=['Clock_Round_','Service_Area_']+[col for col in table.columns if 'bid' in col]

#change the columns names to only TSP
winbid=table[winbid_columns]
winbid.columns=winbid.columns.str.lstrip('prov_win_bid_') 
winbid=winbid.rename(columns={'Clock_Round_':'Clock_Round','Service_Area_':'Service_Area'})

#second frame contcains purely ranks;change the columns names to only TSP
winrank=table[winrank_columns]
winrank.columns=winrank.columns.str.lstrip('prov_rank_')
winrank=winrank.rename(columns={'Clock_Round_':'Clock_Round','Service_Area_':'Service_Area'})
 

col4, col5 = st.columns([2,4])
with col4:
   plot_type = st.radio(
    "Select the graph type",
    (":green[Line Graph]",  ":blue[Heat Map]"),
    )
with col5:
    LSAS= st.multiselect('Choose LSA:',options=lsa_names, default = lsa_names[0])

st.divider()

#states=winbid.Service_Area.unique()   
    
dframe=read_blocks(auction_year,auction_band)
dframe=dframe.set_index('LSA')

if plot_type == ":green[Line Graph]":
    #st.write("You selected Linegraph.")
    
    states=LSAS
    
    for state in states:  
        #first no of blocks in the LSA
        blok=dframe.query('LSA==@state').values[0][0] 
            
        # now filter the plotting data
        winbid_play=winbid.query('Service_Area==@state')
    
        if winbid_play.shape[0]>8: 
            winbid_play=winbid_play.iloc[-50:]   
        else: #only few LSA are less than 15
            winbid_play=winbid_play.iloc[0:]   
        kind='Bid Value'      
        (winbid_play.pipe(plotly_plot,state,kind,blok))

    st.divider()

    #states=winrank.Service_Area.unique()
    for state in states:   
        #first no of blocks in the LSA
        blok=dframe.query('LSA==@state').values[0][0]   
       
        # now filter the plotting data
       
        winrank_play=winrank.query('Service_Area==@state') 
        if winrank_play.shape[0]>8: 
            winrank_play=winrank_play.iloc[0:]   
        else: #only few LSA are less than 15
            winrank_play=winrank_play.iloc[0:] 
        kind='Bid Rank'            
        (winrank_play.pipe(plotly_plot,state,kind,blok))
    


else:
    #st.write("You selected Heatmap.")
    #For bid amount heatmap
    #states=winbid.Service_Area.unique()
    states=LSAS
    for state in states:
        #first no of blocks in the LSA
        blok=dframe.query('LSA==@state').values[0][0] 
            
        # now filter the plotting data
        winbid_play=winbid.query('Service_Area==@state')
        if winbid_play.shape[0]>8: 
            winbid_play=winbid_play.iloc[-50:]   
        else: #only few LSA are less than 15
            winbid_play=winbid_play.iloc[0:] 
        kind='Bid Value'      
        (winbid_play.pipe(plotly_imshow,state,kind,blok))

    st.divider()

    #For bid rank heatmap
    #states=winrank.Service_Area.unique()
    for state in states:  
        #first no of blocks in the LSA
        blok=dframe.query('LSA==@state').values[0][0] 
            
        # now filter the plotting data
        winrank_play=winrank.query('Service_Area==@state')
        if winrank_play.shape[0]>8: 
            winrank_play=winrank_play.iloc[0:]   
        else: #only few LSA are less than 15
            winrank_play=winrank_play.iloc[0:]  
        kind='Bid Rank'     
        (winrank_play.pipe(plotly_imshow,state,kind,blok))