import pandas as pd
import copy
import sqlite3 as sq
from py5paisa import FivePaisaClient
import yfinance as yf
import Database as db
import datetime as dt

def get_full_data():
    cred={
        "APP_NAME":"5P55638300",
        "APP_SOURCE":"9216",
        "USER_ID":"NQt3w6KdIS0",
        "PASSWORD":"CCByL3QGV4i",
        "USER_KEY":"zIImBvHQcKS37KNbefLn5NOs6ioiYACm",
        "ENCRYPTION_KEY":"QXcUSr0dNFc3GdSC0FLQpwG2pYGggTmY"
        }
    
    client = FivePaisaClient(cred=cred)
    
    # OAUTH Approach
    # First get a token by logging in to -> https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey=zIImBvHQcKS37KNbefLn5NOs6ioiYACm&ResponseURL=localhost
    # VendorKey is UesrKey for individuals user
    # for e.g. you can use ResponseURL as https://www.5paisa.com/technology/developer-apis
    # Pass the token received in the response url after successful login to get an access token (this also sets the token for all the APIs you use)-
    # Please note that you need to copy the request token from URL and paste in this code and start the code within 30s.
    #client.get_oauth_session('Your Response Token')
    
    client.get_oauth_session('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjU1NjM4MzAwIiwicm9sZSI6InpJSW1CdkhRY0tTMzdLTmJlZkxuNU5PczZpb2lZQUNtIiwiU3RhdGUiOiIiLCJuYmYiOjE3MTQ4MzM2ODcsImV4cCI6MTcxNDgzNzI4NywiaWF0IjoxNzE0ODMzNjg3fQ.vtWteKlgOeGt4BlD-639YzS0Hny3TYjDBsFYxLimkNk')
    
    #historical_data(exchange,exchange type,scrip code,time frame,from data,to date)
    #https://images.5paisa.com/website/scripmaster-csv-format.csv
    # Note : TimeFrame Should be from this list ['1m','5m','10m','15m','30m','60m','1d']
    
    df_nse_100 = pd.read_csv("C:/NSE/STOCKS/ind_nifty500list_V1.csv")
    ohlcv = {}
    for index, row in df_nse_100.iterrows():
        print(row['Symbol'], row['sccode'])
        #print(df1)
        df1=client.historical_data('N','C',row['sccode'],'1d','2010-12-17','2011-06-16')
        #print(df1)
        df2=client.historical_data('N','C',row['sccode'],'1d','2011-06-17','2011-12-16')

        #print(df1)
        df3=client.historical_data('N','C',row['sccode'],'1d','2011-12-17','2012-06-16')
        #print(df1)
        df4=client.historical_data('N','C',row['sccode'],'1d','2012-06-17','2012-12-16')

        #print(df1)
        df5=client.historical_data('N','C',row['sccode'],'1d','2012-12-17','2013-06-16')
        #print(df1)
        df6=client.historical_data('N','C',row['sccode'],'1d','2013-06-17','2013-12-16')

        #print(df1)
        df7=client.historical_data('N','C',row['sccode'],'1d','2013-12-17','2014-06-16')
        #print(df1)
        df8=client.historical_data('N','C',row['sccode'],'1d','2014-06-17','2014-12-16')
        #print(df1)
        df9=client.historical_data('N','C',row['sccode'],'1d','2014-12-17','2015-06-16')
        #print(df1)
        df10=client.historical_data('N','C',row['sccode'],'1d','2015-06-17','2015-12-16')

        #print(df1)
        df11=client.historical_data('N','C',row['sccode'],'1d','2015-12-17','2016-06-16')
        #print(df1)
        df12=client.historical_data('N','C',row['sccode'],'1d','2016-06-17','2016-12-16')
        #print(df1)
        df13=client.historical_data('N','C',row['sccode'],'1d','2016-12-17','2017-06-16')
        #print(df1)
        df14=client.historical_data('N','C',row['sccode'],'1d','2017-06-17','2017-12-16')        
        #print(df1)
        df15=client.historical_data('N','C',row['sccode'],'1d','2017-12-17','2018-06-16')
        #print(df1)
        df16=client.historical_data('N','C',row['sccode'],'1d','2018-06-17','2018-12-16')
        
        #print(df1)
        df17=client.historical_data('N','C',row['sccode'],'1d','2018-12-17','2019-06-16')
        #print(df1)
        df18=client.historical_data('N','C',row['sccode'],'1d','2019-06-17','2019-12-16')        
        
        #print(df1)
        df19=client.historical_data('N','C',row['sccode'],'1d','2019-12-17','2020-06-16')
        #print(df1)
        df20=client.historical_data('N','C',row['sccode'],'1d','2020-06-17','2020-12-16')
                
        #print(df1)
        df21=client.historical_data('N','C',row['sccode'],'1d','2020-12-17','2021-06-16')
        #print(df1)
        df22=client.historical_data('N','C',row['sccode'],'1d','2021-06-17','2021-12-16')
        #print(df2)
        df23=client.historical_data('N','C',row['sccode'],'1d','2021-12-17','2022-06-16')
        #print(df3)
        df24=client.historical_data('N','C',row['sccode'],'1d','2022-06-17','2022-12-16')
        #print(df4)
        df25=client.historical_data('N','C',row['sccode'],'1d','2022-12-17','2023-06-16')
        #print(df5)
        df26=client.historical_data('N','C',row['sccode'],'1d','2023-06-17','2023-12-16')
        #print(df6)
        df27=client.historical_data('N','C',row['sccode'],'1d','2023-12-17','2024-05-02')
        #print(df7)
        #df28=client.historical_data('N','C',row['sccode'],'1d','2024-06-17','2024-12-16')
        #print(df4)
        #df29=client.historical_data('N','C',row['sccode'],'1d','2024-12-17','2025-06-16')
        #print(df5)
        #df30=client.historical_data('N','C',row['sccode'],'1d','2025-06-17','2025-12-16')
        #print(df6)
        #df31=client.historical_data('N','C',row['sccode'],'1d','2025-12-17','2026-03-02')
        #print(df7)
      
        
      
        
      
        
      
        df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10,
                        df11, df12, df13, df14, df15, df16, df17, df18,df19,  df20,
                        df21, df22, df23, df24, df25, df26, df27    ], ignore_index=True)
        ohlcv[row['Symbol']] = df
   
    tickers = df_nse_100["Symbol"].to_list()
    df = copy.deepcopy(ohlcv)
    df_full = pd.DataFrame()
   
    for ticker in tickers:
      if len(df[ticker]) > 80:
        print("merging for ",ticker)
        ohlcv[ticker]["ticker"] = ticker
        ohlcv[ticker]["Date"] = ohlcv[ticker].index
        df_full = pd.concat( [ df_full , ohlcv[ticker] ]  )
   
    sql_data = 'C:\\NSE\\SA.sqlite2'
    conn = sq.connect(sql_data)
    cur = conn.cursor()
    
    cur.execute('''DROP TABLE IF EXISTS TAB_ANA''')
    cur.execute('''DROP TABLE IF EXISTS N100_OHLC_1D''')
    
    df_full.to_sql('N100_OHLC_1D', conn, if_exists='replace', index=True) # - writes the pd.df to SQLIte DB
    
    cur.execute('COMMIT')



def get_delta_data():

    df = db.get_data("""select ticker, DATE(substr(MAX(DATETIME),1,10),'+1 days') START_DATE
     from N100_OHLC_1D 
     group by ticker""" )
        
    df_full = pd.DataFrame()
    for index, row in df.iterrows():
        print(row['ticker'],row['START_DATE'])
        
        if dt.datetime.strptime(row['START_DATE'], '%Y-%m-%d').date() >= dt.datetime.today().date(): 
            print('UptoDate')
        else:    
            data = yf.download(row['ticker'] + '.NS' , row['START_DATE'], dt.datetime.today() , interval="1d")    
            
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
        df_full['Date'] = ""
        df_full = df_full[['Datetime','Open','High','Low','Close','Volume','ticker','Date']]
        db.insert_data('N100_OHLC_1D', df_full)
    return 'ALL DONE'


# delete from N100_OHLC_1D  where rowid in (
# select  max(ROWID)
# from N100_OHLC_1D a group by ticker,datetime HAVING COUNT(1)>1)

