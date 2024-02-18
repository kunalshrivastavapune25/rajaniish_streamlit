import streamlit as st
import pandas

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)


with col1:
    st.image("images/photo.png")

with col2:
    st.title("Kunal Shrivastava")
    content = """
    Welcome to my website! I'm Kunal Shrivastava, a Python programmer and enthusiastic algo trading aficionado. Here, you'll find a consolidated showcase of my endeavors in trading strategy backtesting, machine learning, and AI applications. This platform owes its richness to the invaluable contributions of notable individuals like Mr. Anand Joshi, Mr. Rahul Phadake, Mr. Gaurav Sirsaj, and a lot of others joining us in this journey..
    """
    st.info(content)

content2 = """
In Home page you can find some of the apps I have built in Python. Feel free to contact me!
"""
st.write(content2)