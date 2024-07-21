import streamlit as st
st.set_page_config(layout="wide",page_title = "This is a Multipage WebApp") 
dotlink = '[Official Website](https://dot.gov.in/spectrum-management/2463)'
col1, mid, col2 = st.columns([2,1,20])
with col1:
    st.image('dot.jpg', width=80)
    
with col2:
    st.write("""## Spectrum Management for Cellular Service """)
st.title("Information on IMT Spectrum .")
# st.markdown("# Main page 🎈")
# st.sidebar.markdown("# Main page 🎈")


#st.sidebar.success("Selection Above") 
col3, col4 = st.columns([70,30])

# with col3:
#     st.image('SMRA.png')


with col3:
    st.markdown(
    """       
    <span style="font-size: 24px;">
    1. Spectrum Holding of all Operators;<br>
    2. Market price of Spectrum for all  operators;<br>
    3. Reserve Price,Selling Price Comparison across all auctions; <br>
    4. Spectrum Shared among operators;<br>
    5. Spectrum Traded among operators;<br>
    6. The auction activity through the provisional bids and ranking;<br>
    7. The plots are interactive to give granularity; 
    </span>
     """, unsafe_allow_html=True )


st.write( """#### """, dotlink)           

col5, col6, col7 = st.columns([40,20,20])
with col6:
    st.markdown("""## :orange[Developed By ]""")
with col7:    
    st.image('logo.png', width=150)