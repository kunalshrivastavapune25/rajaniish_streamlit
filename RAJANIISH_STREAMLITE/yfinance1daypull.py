import pandas as pd
import copy
import sqlite3 as sq

import yfinance as yf
import Database as db
import datetime as dt
import yfinance as yf

    
df_nse_500 = pd.read_csv("C:/NSE/STOCKS/ind_nifty500list_V1.csv")
ohlcv = {}
for index, row in df_nse_500.iterrows():
    print(row['Symbol'] + '.NS')
    df1=yf.download(row['Symbol'] + '.NS', period='100mo', interval="1d")
    ohlcv[row['Symbol']] = df1
   
tickers = df_nse_500["Symbol"].to_list()
df = copy.deepcopy(ohlcv)
df_full = pd.DataFrame()
   
for ticker in tickers:
    if len(df[ticker]) > 80:
        print("merging for ",ticker)
        ohlcv[ticker]["ticker"] = ticker
        ohlcv[ticker]["Datef"] = ohlcv[ticker].index    
        ohlcv[ticker]["Change_Pct"]= ohlcv[ticker]["High"].pct_change() * 100 
        df_full = pd.concat( [ df_full , ohlcv[ticker] ]  )
df_full.reset_index(inplace=True)

df_full = df_full.drop(columns=['Date'])

sql_data = 'C:\\NSE\\SA.sqlite2'
conn = sq.connect(sql_data)
cur = conn.cursor()
    
cur.execute('''DROP TABLE IF EXISTS TAB_ANA''')
cur.execute('''DROP TABLE IF EXISTS N500_OHLC''')

df_full.to_sql('N500_OHLC', conn, if_exists='replace', index=True) # - writes the pd.df to SQLIte DB

cur.execute('COMMIT')



