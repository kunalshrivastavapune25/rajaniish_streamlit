import streamlit as st
import pandas as pd
import numpy as np
import nsepython as npy
import DeltaDisp as dd
import Database as db
import pull_nse100 as pn100
import pull_nseindex as pnidx
st.set_page_config(layout="wide")

@st.cache_data
def get_data_dd(security_name):
    σ = get_iv()
    p = npy.quote_derivative(security_name)
    df = dd.calculate_deltas(σ,p)
    return df

@st.cache_data
def get_iv():
    σ = npy.indiavix()
    return σ


if st.session_state["authentication_status"]:
    
 

    st.markdown("#### Delta Disparity")
    with st.expander("Click to Expand"):
        if st.button(label="Check", key="eqbutton11"):
            df = pd.concat([get_data_dd('ITC'),get_data_dd('SBIN'),
                            get_data_dd('HDFCBANK')])
            df = df.reset_index(drop=True)
            st.dataframe(data= df,hide_index=True)
        
       #with st.form("population-form"):
         
            # col1, col2, col3 = st.columns(3)
            # with col1:
            #     st.text_input("Enter Expiry Date:" ,placeholder="2023-12-28")
            #     st.text_input("CE:" ,placeholder="+0.17")

            # with col2:
            #     st.text_input("Enter Interest:" ,placeholder="7.1497")
            #     st.text_input("PE:" ,placeholder="-0.17")

            # with col3:
            #     st.text_input("Stock File:" ,placeholder="")
            #     st.text_input("Op File:" ,placeholder="")
            # submit_btn = st.form_submit_button("Generate", type="primary")


    st.markdown("#### Do Not Execute")
    with st.expander("Click to Expand"):


        ini_val = """select 'Nifty100' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
         MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
         from N100_OHLC
        UNION
        select 'NiftyINDEX' as DATA, count(distinct ticker) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
         MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
         from NINDEX_OHLC
         UNION
         select * from tab_summary
         UNION
        select 'niftyoptions' as DATA, count(distinct strike_price) INSTRUMENT_CNT, COUNT(1) TOTAL_DATA_CNT,
         MIN(DATETIME) START_DATE, MAX(DATETIME) END_DATE
         from nniftyoptions_ohlc"""
        equity_query =  st.text_area(label="Status",value=ini_val)
        

        if st.button(label="Check", key="eqbutton"):
            st.dataframe(data= db.get_data(equity_query)  ,hide_index=True,use_container_width=True)
        if st.button(label="Update ALL Tables to till Date", key="eqrefbutton"):
            rstr = pn100.get_delta_data()
            rstr1 = pnidx.get_delta_data()
            rstr2 = db.resample_tabs()
            # st.write(rstr + ' for N100')
            # st.write(rstr1 + ' for NINDEX')
            st.dataframe(data= db.get_data(equity_query)  ,hide_index=True,use_container_width=True)
        # if st.button(label="Check 1day,1hr,15m tables", key="TABbutton"):
        #     df_full_tabs = db.get_data("select * from tab_summary" )
        #     st.write(df_full_tabs)
        # if st.button(label="Recreate 1day,1hr,15m tables", key="TABbutton1"):     
                    
        #     rstr = db.resample_tabs()
            st.success('Done')

    st.markdown("#### Tables Details")
    with st.expander("Click to Expand"):
       
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown("**Category**")
            st.write('Nifty100')
            st.write('Nifty100')
            st.write('Nifty100')
            st.write('Nifty100')
            st.write('INDEX')
            st.write('INDEX')            
            st.write('INDEX')
            st.write('INDEX')
            st.write('NIFTYOPT')
            st.write('NIFTYOPT')            
            st.write('NIFTYOPT')
            st.write('NIFTYOPT')
            
        with col2:
            st.write('StartDate')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')         
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')            
            st.write('2010-01-01')
            st.write('2010-01-01')
    
        with col3:
            st.write('EndDate')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')         
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')
            st.write('2010-01-01')            
            st.write('2010-01-01')
            st.write('2010-01-01')        
        with col4:
            st.write('Interval')
            st.write('1 Day')
            st.write('1 Hour')
            st.write('15 Min')
            st.write('5 Min')
            st.write('1 Day')
            st.write('1 Hour')         
            st.write('15 Min')
            st.write('5 Min')
            st.write('1 Day')
            st.write('1 Hour')            
            st.write('15 Min')
            st.write('5 Min')

        with col5:
            st.write('Refresh')
            st.button('Refresh N100',key='1')
            st.button('Refresh NIndex',key='2')
            st.button('Refresh NOptions',key='3')
           
            
            
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')