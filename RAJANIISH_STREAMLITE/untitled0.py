import streamlit as st
import pandas as pd
import numpy as np
import nsepython as npy

import Database as db
import pull_nse100 as pn100
import pull_nseindex as pnidx

df_entry = pd.DataFrame()

sql_data = 'C:\\NSE\\SA.sqliteanand' #- Creates DB names SQLite

df_entry = pd.read_csv ('C:\\Users\\kush0221\\Downloads\\entry.csv')
df_exit = pd.read_csv ('C:\\Users\\kush0221\\Downloads\\exit_bb.csv')

db.insert_data('entry_tab',df_entry,sql_data)

db.insert_data('exit_tab',df_exit,sql_data)