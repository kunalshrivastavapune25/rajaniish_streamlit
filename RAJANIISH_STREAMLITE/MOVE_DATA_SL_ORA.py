import Database as db
import pandas as pd
import sqlite3 as sq



df = pd.DataFrame()



df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from N100_OHLC_15M')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTY100_15M')
df.to_sql('N100_OHLC_15M', conn , if_exists='replace', index=False)


df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from N100_OHLC')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTY100_5M')
df.to_sql('N100_OHLC_5M', conn , if_exists='replace', index=False)

df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from N100_OHLC_1H')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTY100_1H')
df.to_sql('N100_OHLC_1H', conn , if_exists='replace', index=False)

df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from N100_OHLC_1D')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTY100_1D')
df.to_sql('N100_OHLC_1D', conn , if_exists='replace', index=False)




df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from NINDEX_OHLC_15M')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTYINDEX_15M')
df.to_sql('NINDEX_OHLC_15M', conn , if_exists='replace', index=False)

df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from NINDEX_OHLC')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTYINDEX_5M')
df.to_sql('NINDEX_OHLC_5M', conn , if_exists='replace', index=False)

df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from NINDEX_OHLC_1H')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTYINDEX_1H')
df.to_sql('NINDEX_OHLC_1H', conn , if_exists='replace', index=False)

df = db.get_data('select Datetime,Open,High,Low,Close,Volume,ticker from NINDEX_OHLC_1D')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NIFTYINDEX_1D')
df.to_sql('NINDEX_OHLC_1D', conn , if_exists='replace', index=False)



df = db.get_data('select * from NNIFTYOPTIONS_OHLC_15M')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_15M')
df.to_sql('NNIFTYOPTIONS_OHLC_15M', conn , if_exists='replace', index=False)

df = db.get_data('select * from NNIFTYOPTIONS_OHLC')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_5M')
df.to_sql('NNIFTYOPTIONS_OHLC_5M', conn , if_exists='replace', index=False)

df = db.get_data('select * from NNIFTYOPTIONS_OHLC_1H')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_1H')
df.to_sql('NNIFTYOPTIONS_OHLC_1H', conn , if_exists='replace', index=False)

df = db.get_data('select * from NNIFTYOPTIONS_OHLC_1D')
conn = sq.connect('C:\\NSE\\SA.sqliteDB_NNIFTYOPTIONS_1D')
df.to_sql('NNIFTYOPTIONS_OHLC_1D', conn , if_exists='replace', index=False)
