import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nsepython as np
import DeltaDisp as dd
st.set_page_config(layout="wide")

@st.cache_data
def get_data_dd(security_name):
    σ = np.indiavix()
    p = np.quote_derivative(security_name)
    df = dd.calculate_deltas(σ,p)
    return df



if st.session_state["authentication_status"]:
    
 

    st.markdown("#### Delta Disparity")
    with st.expander("Click to Expand"):
        df = pd.concat([get_data_dd('ITC'),get_data_dd('SBIN'),
                        get_data_dd('HDFCBANK')])
        st.write(df)
        
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


    st.divider()

    st.markdown("#### Price Tracker")
    with st.expander("Click to Expand"):
        with st.form("population-form1"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("Choose a starting date")
            with col2:
                st.write("Choose an end date")
            with col3:
                st.write("Choose a location")
            submit_btn = st.form_submit_button("Analyze", type="primary")







elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')