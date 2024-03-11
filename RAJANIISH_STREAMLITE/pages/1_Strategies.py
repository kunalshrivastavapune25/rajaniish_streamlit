import streamlit as st
import pandas as pd
import nsepython as npy
import DeltaDisp as dd
import Database as db
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

try:
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
    
    
    
        with st.expander("NIFTY100_15M"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from N100_OHLC_15M group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTY100_15M')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NIFTY100_5M"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from N100_OHLC_5M group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTY100_5M')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NIFTY100_1H"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from N100_OHLC_1H group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTY100_1H')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NIFTY100_1D"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from N100_OHLC_1D group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTY100_1D')  ,hide_index=True,use_container_width=True)
    
    
    
    
        with st.expander("NINDEX_15M"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NINDEX_OHLC_15M group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_15M')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NINDEX_5M"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NINDEX_OHLC_5M group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_5M')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NINDEX_1H"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NINDEX_OHLC_1H group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_1H')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NINDEX_1D"):
            st.dataframe(data= db.get_data("""select ticker, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NINDEX_OHLC_1D group by ticker""",
    'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_1D')  ,hide_index=True,use_container_width=True)
            
    
    
    
        with st.expander("NNIFTYOPTIONS_15M"):
            st.dataframe(data= db.get_data("""select expiry_date, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NNIFTYOPTIONS_OHLC_15M group by expiry_date""",
    'C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_15M')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NNIFTYOPTIONS_5M"):
            st.dataframe(data= db.get_data("""select expiry_date, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NNIFTYOPTIONS_OHLC_5M group by expiry_date""",
    'C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_5M')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NNIFTYOPTIONS_1H"):
            st.dataframe(data= db.get_data("""select expiry_date, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NNIFTYOPTIONS_OHLC_1H group by expiry_date""",
    'C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_1H')  ,hide_index=True,use_container_width=True)
    
        with st.expander("NNIFTYOPTIONS_1D"):
            st.dataframe(data= db.get_data("""select expiry_date, COUNT(1) total_records , 
    MAX(datetime(datetime)) as to_date, MIN(datetime(datetime)) as from_date 
    from NNIFTYOPTIONS_OHLC_1D group by expiry_date""",
    'C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_1D')  ,hide_index=True,use_container_width=True)
            
    
                
                
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
except KeyError:
    # If KeyError occurs, display a message to sign in
    st.warning('Please sign in.')        