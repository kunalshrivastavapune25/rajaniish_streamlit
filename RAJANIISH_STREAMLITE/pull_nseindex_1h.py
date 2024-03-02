import pandas as pd
import copy
import sqlite3 as sq
import Database as db
from py5paisa import FivePaisaClient
import datetime as dt
import yfinance as yf


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
    
    client.get_oauth_session('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjU1NjM4MzAwIiwicm9sZSI6InpJSW1CdkhRY0tTMzdLTmJlZkxuNU5PczZpb2lZQUNtIiwiU3RhdGUiOiIiLCJuYmYiOjE3MDg1NjY0ODMsImV4cCI6MTcwODU2NjU0MywiaWF0IjoxNzA4NTY2NDgzfQ.loUrf0a48DqJ2UlSfXHNWPwZu4oEV16praUEqt9hack')
    
    #historical_data(exchange,exchange type,scrip code,time frame,from data,to date)
    #https://images.5paisa.com/website/scripmaster-csv-format.csv
    # Note : TimeFrame Should be from this list ['1m','5m','10m','60m','30m','60m','1d']
    

    df_nse_100 = pd.read_csv("C:/NSE/STOCKS/ind_index.csv")
    ohlcv = {}
    for index, row in df_nse_100.iterrows():
        print(row['Symbol'], row['sccode'])
        #print(df1)
        df1=client.historical_data('N','C',row['sccode'],'60m','2010-12-17','2011-06-16')
        #print(df1)
        df2=client.historical_data('N','C',row['sccode'],'60m','2011-06-17','2011-12-16')

        #print(df1)
        df3=client.historical_data('N','C',row['sccode'],'60m','2011-12-17','2012-06-16')
        #print(df1)
        df4=client.historical_data('N','C',row['sccode'],'60m','2012-06-17','2012-12-16')

        #print(df1)
        df5=client.historical_data('N','C',row['sccode'],'60m','2012-12-17','2013-06-16')
        #print(df1)
        df6=client.historical_data('N','C',row['sccode'],'60m','2013-06-17','2013-12-16')

        #print(df1)
        df7=client.historical_data('N','C',row['sccode'],'60m','2013-12-17','2014-06-16')
        #print(df1)
        df8=client.historical_data('N','C',row['sccode'],'60m','2014-06-17','2014-12-16')
        #print(df1)
        df9=client.historical_data('N','C',row['sccode'],'60m','2014-12-17','2015-06-16')
        #print(df1)
        df10=client.historical_data('N','C',row['sccode'],'60m','2015-06-17','2015-12-16')

        #print(df1)
        df11=client.historical_data('N','C',row['sccode'],'60m','2015-12-17','2016-06-16')
        #print(df1)
        df12=client.historical_data('N','C',row['sccode'],'60m','2016-06-17','2016-12-16')
        #print(df1)
        df13=client.historical_data('N','C',row['sccode'],'60m','2016-12-17','2017-06-16')
        #print(df1)
        df14=client.historical_data('N','C',row['sccode'],'60m','2017-06-17','2017-12-16')        
        #print(df1)
        df15=client.historical_data('N','C',row['sccode'],'60m','2017-12-17','2018-06-16')
        #print(df1)
        df16=client.historical_data('N','C',row['sccode'],'60m','2018-06-17','2018-12-16')
        
        #print(df1)
        df17=client.historical_data('N','C',row['sccode'],'60m','2018-12-17','2019-06-16')
        #print(df1)
        df18=client.historical_data('N','C',row['sccode'],'60m','2019-06-17','2019-12-16')        
        
        #print(df1)
        df18=client.historical_data('N','C',row['sccode'],'60m','2019-12-17','2020-06-16')
        #print(df1)
        df20=client.historical_data('N','C',row['sccode'],'60m','2020-06-17','2020-12-16')
                
        #print(df1)
        df21=client.historical_data('N','C',row['sccode'],'60m','2020-12-17','2021-06-16')
        #print(df1)
        df22=client.historical_data('N','C',row['sccode'],'60m','2021-06-17','2021-12-16')
        #print(df2)
        df23=client.historical_data('N','C',row['sccode'],'60m','2021-12-17','2022-06-16')
        #print(df3)
        df24=client.historical_data('N','C',row['sccode'],'60m','2022-06-17','2022-12-16')
        #print(df4)
        df25=client.historical_data('N','C',row['sccode'],'60m','2022-12-17','2023-06-16')
        #print(df5)
        df26=client.historical_data('N','C',row['sccode'],'60m','2023-06-17','2023-12-16')
        #print(df6)
        df27=client.historical_data('N','C',row['sccode'],'60m','2023-12-17','2024-03-02')
        #print(df7)
        
        df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10,
                        df11, df12, df13, df14, df15, df16, df17, df18,  df20,
                        df21, df22, df23, df24, df25, df26, df27], ignore_index=True)
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
    
    
    cur.execute('''DROP TABLE IF EXISTS NINDEX_OHLC_1H''')
    
    df_full.to_sql('NINDEX_OHLC_1H', conn, if_exists='replace', index=True) # - writes the pd.df to SQLIte DB


def get_delta_data():

    df = db.get_data("""select ticker, DATE(substr(MAX(DATETIME),1,10),'+1 days') START_DATE
     from NINDEX_OHLC 
     group by ticker""" )
        
    df_full = pd.DataFrame()
    for index, row in df.iterrows():
        print(row['ticker'],row['START_DATE'])
        
        if dt.datetime.strptime(row['START_DATE'], '%Y-%m-%d').date() >= dt.datetime.today().date(): 
            print('UptoDate')
        else:    
            data = yf.download(row['ticker'].replace('BANKNIFTY', '^NSEBANK').replace('NIFTY', '^NSEI') , row['START_DATE'], dt.datetime.today() , interval="5m")    
            
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
        db.insert_data('NINDEX_OHLC', df_full)
    return 'ALL DONE'
    
