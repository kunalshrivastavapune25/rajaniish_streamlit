from breeze_connect import BreezeConnect
breeze = BreezeConnect(api_key="92w862n1o9v1y1562263x0O801T0i0e3")
import numpy as np
import urllib
import datetime
import pandas as pd
#from datetime import datetime, timedelta
import sqlite3 as sq
#import mibian

print("https://api.icicidirect.com/apiuser/login?api_key="+urllib.parse.quote_plus("92w862n1o9v1y1562263x0O801T0i0e3"))



# Generate Session
breeze.generate_session(api_secret="q7c132Q68087876e5z30042l331bD03Y",
                        session_token="35395957")

# Generate ISO8601 Date/DateTime String
iso_date_string = datetime.datetime.strptime("28/02/2021","%d/%m/%Y").isoformat()[:10] + 'T05:30:00.000Z'
iso_date_time_string = datetime.datetime.strptime("05/01/2024 23:59:59","%d/%m/%Y %H:%M:%S").isoformat()[:19] + '.000Z'
print(iso_date_time_string)
breeze.ws_connect()


sql_data = 'C:\\NSE\\SA.sqlite2' #- Creates DB names SQLite
conn = sq.connect(sql_data)
cur = conn.cursor()

#cur.execute('''DROP TABLE IF EXISTS df_o''')



#df_full.to_sql('df_f', conn, if_exists='replace', index=True) # - writes the pd.df to SQLIte DB

NIFTY_OPTIONS_SCP = pd.read_sql_query('select * from NIFTY_OPTIONS_SCP', conn)

NIFTY_OPTIONS_SCP_head = NIFTY_OPTIONS_SCP




NIFTY_OPTIONS_SCP_head['start_date'] = pd.to_datetime(NIFTY_OPTIONS_SCP_head['start_date'], format='%Y-%m-%d')
NIFTY_OPTIONS_SCP_head['start_date'] = NIFTY_OPTIONS_SCP_head['start_date'].apply(lambda x: x.isoformat()[:10] + 'T05:30:00.000Z')

NIFTY_OPTIONS_SCP_head['end_date'] = pd.to_datetime(NIFTY_OPTIONS_SCP_head['expiry_date'], format='%Y-%m-%d')
NIFTY_OPTIONS_SCP_head['end_date'] = NIFTY_OPTIONS_SCP_head['end_date'].apply(lambda x: x.isoformat()[:10] + 'T05:30:00.000Z')



NIFTY_OPTIONS_SCP_head['expiry_date'] = pd.to_datetime(NIFTY_OPTIONS_SCP_head['expiry_date'], format='%Y-%m-%d')

NIFTY_OPTIONS_SCP_head['expiry_date'] = NIFTY_OPTIONS_SCP_head['expiry_date'].apply(lambda x: x.isoformat()[:10] + 'T05:30:00.000Z')


NIFTY_OPTIONS_SCP_head['CP'] =NIFTY_OPTIONS_SCP_head['CP'].str.lower()



max_attempts = 5
i = 0

#########################################################################################
df_full = pd.DataFrame()
a = 0
for index, row in NIFTY_OPTIONS_SCP_head.iterrows():
    print(row['expiry_date'],row['start_date'],row['expiry_date'],row['sp'],row['CP'])
    print(a)
    i = 0
    while i < max_attempts:
        try:       
            response = breeze.get_historical_data(interval="5minute",
                                        from_date= row['start_date'],
                                        to_date= row['expiry_date'],
                                        stock_code="NIFTY",
                                        exchange_code="NFO",
                                        product_type="options",
                                        expiry_date=row['expiry_date'],
                                        right = row['CP'],
                                        strike_price=row['sp'])
            print('atm call pass')
            break
        except:    
            print('atm call failed')
            i += 1
    success_data = response['Success']
    dfs = pd.DataFrame(success_data)
    df_full = pd.concat([df_full, dfs], ignore_index=True)
    a = a+1




df_full.to_sql('df_f', conn, if_exists='replace', index=True) # - writes the pd.df to SQLIte DB



cur.execute('''DROP TABLE IF EXISTS df_o''')


df.to_sql('df_o', conn, if_exists='replace', index=True) # - writes the pd.df to SQLIte DB

cur.execute('''DROP TABLE IF EXISTS df_f''')


df_full.to_sql('df_f', conn, if_exists='replace', index=True) # - writes the pd.df to SQLIte DB



conn.close()
