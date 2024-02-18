import streamlit as st
import pandas
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

col3, empty_col, col4 = st.columns([1.5, 0.05, 1.5])

df = pandas.read_csv("BackTest.csv", sep=";")

with col3:
    for index, row in df[:1].iterrows():
        st.header(row["title"])
        st.write(row["description"])
        st.image("images/" + row["image"])
        st.write(f"[Source Code]({row['url']})")


with col4:
    for index, row in df[1:].iterrows():
        st.header(row["title"])
        st.write(row["description"])
        st.image("images/" + row["image"])
        st.write(f"[Source Code]({row['url']})")