import streamlit as st
import pandas as pd
import numpy as np
import DeltaDisp as dd
st.set_page_config(layout="wide")

@st.cache_data
def get_data_dd(security_name):
    σ = get_iv()
    p = np.quote_derivative(security_name)
    df = dd.calculate_deltas(σ,p)
    return df

@st.cache_data
def get_iv():
    σ = np.indiavix()
    return σ


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

    st.markdown("#### History Details")
    with st.expander("Click to Expand"):
        with st.form("population-form1"):
            col1, col2, col3, col4  = st.columns(4)
            with col1:
                st.write("Equity")
                st.write("Index")
                st.write("Options")                
            with col2:
                options = ['Option 1', 'Option 2', 'Option 3']
                options1 = ['Option 1', 'Option 2', 'Option 3']
                options2 = ['Option 1', 'Option 2', 'Option 3']
                selected_option = st.selectbox('Select an option:', options , key = '1' )
                selected_option1 = st.selectbox('Select an option:', options1 , key = '2')
                selected_option2 = st.selectbox('Select an option:', options2 , key = '3' )
            with col3:
                options3 = ['Option 1', 'Option 2', 'Option 3']
                options4 = ['Option 1', 'Option 2', 'Option 3']
                options5 = ['Option 1', 'Option 2', 'Option 3']
                selected_option3 = st.selectbox('Select an option:', options3, key = '4')
                selected_option4 = st.selectbox('Select an option:', options4, key = '5')
                selected_option5 = st.selectbox('Select an option:', options5, key = '6')
            with col4:
                options6 = ['Option 1', 'Option 2', 'Option 3']
                options7 = ['Option 1', 'Option 2', 'Option 3']             
                selected_option6 = st.selectbox('Select an option:', options6, key = '7')
                selected_option7 = st.selectbox('Select an option:', options7, key = '8')

            submit_btn = st.form_submit_button("OK", type="primary")







elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')