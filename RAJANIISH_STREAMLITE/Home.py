import streamlit as st
import pandas
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


st.set_page_config(
    page_title="Homepage",
    page_icon="🏡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Open YAML file

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login(location='sidebar')

if st.session_state["authentication_status"]:
    authenticator.logout()
    st.markdown(f'#### Welcome *{st.session_state["name"]}*')

    # col1, col2 = st.columns(2)

    # col3, empty_col, col4 = st.columns([1.5, 0.05, 1.5])

    # df = pandas.read_csv("Strategies_data.csv", sep=";")

    # with col3:
    #     for index, row in df[:1].iterrows():
    #         st.subheader(row["title"])
    #         st.write(row["description"])
    #         st.image("images/" + row["image"], width=200)
    #         st.write(f"[Source Code]({row['url']})")


    # with col4:
    #     for index, row in df[1:].iterrows():
    #         st.subheader(row["title"])
    #         st.write(row["description"])
    #         st.image("images/" + row["image"], width=200)
    #         st.write(f"[Source Code]({row['url']})")
    
    



    
    # Add an image at full width
    st.image("Capture.JPG", width=None)
    
    # Add some text



elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')