import pandas as pd
import Database as db
import datetime as dt
import yfinance as yf
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_delta_data(TABLE_NAME ,DB_NAME ,INTERVAL ):
    
   
    df = db.get_data("""select ticker, DATETIME(MAX(DATETIME(DATETIME))) START_DATE
     from """ + TABLE_NAME + """
     group by ticker""" ,DB_NAME)
        
    df_full = pd.DataFrame()
    for index, row in df.iterrows():
        if dt.datetime.today().weekday() in [5, 6]:  # Saturday (5) or Sunday (6)
            mod_date = (dt.datetime.today() - dt.timedelta(days=1)).date()
        else:
            mod_date = dt.datetime.today().date()
        if dt.datetime.strptime(row['START_DATE'], '%Y-%m-%d %H:%M:%S').date() >= mod_date: 
            pass
        else:    
            start_date = row['START_DATE'].strip()  # Remove leading and trailing whitespace
            start_date_formatted = dt.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d') 
            end_date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current date and time
            end_date_formatted = dt.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            sname = row['ticker'] + '.NS'
            sname_formatted =  sname.replace('BANKNIFTY.NS', '^NSEBANK').replace('NIFTY.NS', '^NSEI') 
            data = yf.download( sname_formatted , start_date_formatted, end_date_formatted , interval=INTERVAL)    
            print(start_date_formatted,end_date_formatted)
            data['ticker'] = row['ticker']
            data['Datetime'] = data.index
            df_full = pd.concat([df_full, data])
    if len(df_full) == 0:
        pass
    else:
        df_full['Datetime'] = df_full['Datetime'].astype(str)
        df_full['Datetime']  = df_full['Datetime'].str.replace('+05:30','')
        df_full['Datetime']  = df_full['Datetime'].str.replace(' ','T')
        df_full.reset_index(drop=True, inplace=True)
        df_full.reset_index(drop=True, inplace=True)
        df_full = df_full[['Datetime','Open','High','Low','Close','Volume','ticker']]
        db.insert_data(TABLE_NAME, df_full,DB_NAME)
    return df_full


df_full_ret =  get_delta_data(TABLE_NAME = 'N100_OHLC_15M', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTY100_15M',
                   INTERVAL = '15m')

df_full_ret =  get_delta_data(TABLE_NAME = 'N100_OHLC_5M', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTY100_5M',
                   INTERVAL = '5m')

df_full_ret =  get_delta_data(TABLE_NAME = 'N100_OHLC_1H', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTY100_1H',
                   INTERVAL = '1H')

df_full_ret =  get_delta_data(TABLE_NAME = 'N100_OHLC_1D', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTY100_1D',
                   INTERVAL = '1D')


df_full_ret =  get_delta_data(TABLE_NAME = 'NINDEX_OHLC_15M', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_15M',
                   INTERVAL = '15m')

df_full_ret =  get_delta_data(TABLE_NAME = 'NINDEX_OHLC_5M', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_5M',
                   INTERVAL = '5m')

df_full_ret =  get_delta_data(TABLE_NAME = 'NINDEX_OHLC_1H', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_1H',
                   INTERVAL = '1H')

df_full_ret =  get_delta_data(TABLE_NAME = 'NINDEX_OHLC_1D', 
                   DB_NAME = 'C:\\NSE\\SA.sqliteDB_NIFTYINDEX_1D',
                   INTERVAL = '1D')



import oracledb
import random
import numpy as np
# Establish connection
connection = oracledb.connect(
    user="admin",
    password="Gudiya@123456",
    dsn="rajaniishdb_high",
    config_dir=r"C:\Tools\Oracle Wallet\Wallet_RAJANIISHDB",
    wallet_location=r"C:\Tools\Oracle Wallet\Wallet_RAJANIISHDB",
    wallet_password="Gudiya@1"
)

# Check connection version
print(connection.version)

# Execute query
cursor = connection.cursor()
try:
    cursor.execute("DROP TABLE random_table")
except:
    pass

cursor.execute("""
    CREATE TABLE random_table (
        id date,
        log_msg VARCHAR(100)
    )
""")


cursor.execute("INSERT INTO random_table VALUES (sysdate,'done')")


connection.commit()











# Close cursor and connection
cursor.close()
connection.close()


