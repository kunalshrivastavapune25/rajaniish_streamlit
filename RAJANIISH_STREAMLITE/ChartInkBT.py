import numpy as np
import pandas as pd
import Database as db
import pandas_ta as pt
sql_data = 'C:\\NSE\\SA.sqlite3' #- Creates DB names SQLite
def atr(DF,n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L']=abs(df['High']-df['Low'])
    df['H-PC']=abs(df['High']-df['Close'].shift(1))
    df['L-PC']=abs(df['Low']-df['Close'].shift(1))
    df['TR']=df[['H-L','H-PC','L-PC']].max(axis=1,skipna=False)
    df['ATR'] = df['TR'].ewm(com=n,min_periods=n).mean()
    return df['ATR']
def supertrend(DF,n,m):
    """function to calculate Supertrend given historical candle data
        n = n day ATR - usually 7 day ATR is used
        m = multiplier - usually 2 or 3 is used"""
    df = DF.copy()
    df['ATR'] = atr(df,n)
    df["B-U"]=((df['High']+df['Low'])/2) + m*df['ATR'] 
    df["B-L"]=((df['High']+df['Low'])/2) - m*df['ATR']
    df["U-B"]=df["B-U"]
    df["L-B"]=df["B-L"]
    ind = df.index
    for i in range(n,len(df)):
        if df['Close'][i-1]<=df['U-B'][i-1]:
            df.loc[ind[i],'U-B']=min(df['B-U'][i],df['U-B'][i-1])
        else:
            df.loc[ind[i],'U-B']=df['B-U'][i]    
    for i in range(n,len(df)):
        if df['Close'][i-1]>=df['L-B'][i-1]:
            df.loc[ind[i],'L-B']=max(df['B-L'][i],df['L-B'][i-1])
        else:
            df.loc[ind[i],'L-B']=df['B-L'][i]  
    df['Strend']=np.nan
    for test in range(n,len(df)):
        if df['Close'][test-1]<=df['U-B'][test-1] and df['Close'][test]>df['U-B'][test]:
            df.loc[ind[test],'Strend']=df['L-B'][test]
            break
        if df['Close'][test-1]>=df['L-B'][test-1] and df['Close'][test]<df['L-B'][test]:
            df.loc[ind[test],'Strend']=df['U-B'][test]
            break
    for i in range(test+1,len(df)):
        if df['Strend'][i-1]==df['U-B'][i-1] and df['Close'][i]<=df['U-B'][i]:
            df.loc[ind[i],'Strend']=df['U-B'][i]
        elif  df['Strend'][i-1]==df['U-B'][i-1] and df['Close'][i]>=df['U-B'][i]:
            df.loc[ind[i],'Strend']=df['L-B'][i]
        elif df['Strend'][i-1]==df['L-B'][i-1] and df['Close'][i]>=df['L-B'][i]:
            df.loc[ind[i],'Strend']=df['L-B'][i]
        elif df['Strend'][i-1]==df['L-B'][i-1] and df['Close'][i]<=df['L-B'][i]:
            df.loc[ind[i],'Strend']=df['U-B'][i]
    return df['Strend']
def BollBnd(DF,n):
    "function to calculate Bollinger Band"
    df = DF.copy()
    df["MA"] = df['Close'].rolling(n).mean()
    df["BB_up"] = df["MA"] + 2*df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] - 2*df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    #df.dropna(inplace=True)
    return df

df = db.get_data('select * from N100_OHLC_1D')
df['Datetime'] = pd.to_datetime(df['Datetime'])
grouped = df.groupby('ticker')
dict_of_dfs = {key: group.reset_index(drop=True) for key, group in grouped}
tickers = dict_of_dfs.keys()

table_name = 'N100_OHLC_1D_FULL'
db.drop_data('N100_OHLC_1D_FULL',sql_data)
for ticker in tickers:
    dict_of_dfs[ticker].dropna(inplace=True)
    if len(dict_of_dfs[ticker]) > 50:
        print("merging for ",ticker)
        df =  dict_of_dfs[ticker]
        df[['Open', 'High','Low','Close']].astype(float)
        #dict_of_dfs[ticker]["ST"] =  supertrend(dict_of_dfs[ticker],7,3)
        dict_of_dfs[ticker]["ST"] = pt.supertrend(df['High'], df['Low'], df['Close'], length=7, multiplier=3)['SUPERT_7_3.0']
        dict_of_dfs[ticker]["BollBnd"] = BollBnd(dict_of_dfs[ticker],20)["BB_up"]
        dict_of_dfs[ticker]["BollBnd_dn"] = BollBnd(dict_of_dfs[ticker],20)["BB_dn"]
        dict_of_dfs[ticker][['lower_band', 'mid', 'upper_band' ]] = pt.bbands(df['Close'], length=20, std=2).iloc[:, :3]

        df =  dict_of_dfs[ticker] 
        db.insert_data(table_name, df,sql_data )

        

#df["ST"] = pt.supertrend(df['High'], df['Low'], df['Close'], length=10, multiplier=3)['SUPERT_' + '10' + '_3.0']

df = pd.read_csv('Backtest Stocks closing below the supertrend line, Technical Analysis Scanner.csv')

db.drop_data('N100_TEST',sql_data)
db.insert_data('N100_TEST', df,sql_data )

#########add column for entry price

db.drop_data('N100_TEST_EP' ,sql_data)
db.execute_qry("""create table N100_TEST_EP as 
          select a.*, (select b.close from N100_OHLC_1D_FULL b 
                       where a.symbol = b.ticker 
                       and date(a.date) = date(b.datetime)) AS EP
          from N100_TEST a """ ,sql_data)
df = db.get_data('SELECT * FROM N100_TEST_EP',sql_data)


#########add column for hit date

db.drop_data('N100_TEST_HD' ,sql_data)
db.execute_qry("""create table N100_TEST_HD as 
          select a.*, (select MIN(date(b.datetime)) 
                       from N100_OHLC_1D_FULL b 
                       where a.symbol = b.ticker 
                       and DATE(a.date) < date(b.datetime) 
                       and cast(b.ST as float) > cast(b.close as float) ) AS HD
          from N100_TEST_EP a """ ,sql_data)

df = db.get_data('SELECT * FROM N100_TEST_HD',sql_data)

#########add column for hit price

db.drop_data('N100_TEST_HP' ,sql_data)
db.execute_qry("""create table N100_TEST_HP as 
          select a.*, (select b.close from N100_OHLC_1D_FULL b 
                       where a.symbol = b.ticker 
                       and date(b.datetime) = date(a.HD) ) AS HP
          from N100_TEST_HD a """ ,sql_data)
df = db.get_data('SELECT * FROM N100_TEST_HP',sql_data)


#########add column for duration

db.drop_data('N100_TEST_D' ,sql_data)
db.execute_qry("""create table N100_TEST_D as 
          select a.*, julianday(date(HD)) - julianday(date( date)) AS D
          from N100_TEST_HP a """ ,sql_data)
df = db.get_data('SELECT * FROM N100_TEST_D',sql_data)

#########add column for maxprice

db.drop_data('N100_TEST_MP' ,sql_data)
db.execute_qry("""create table N100_TEST_MP as 
          select a.*, (select MAX(b.close) from N100_OHLC_1D_FULL b 
                       where a.symbol = b.ticker 
                       and  date(b.datetime)  between date(a.date) and date( a.HD)  ) AS MP
          from N100_TEST_D a """ ,sql_data)
df = db.get_data('SELECT * FROM N100_TEST_MP',sql_data)

#########add column for minprice

db.drop_data('N100_TEST_MNP' ,sql_data)
db.execute_qry("""create table N100_TEST_MNP as 
          select a.*, (select MIN(b.close) from N100_OHLC_1D_FULL b 
                       where a.symbol = b.ticker 
                       and  date(b.datetime)  between date(a.date) and date( a.HD)) AS MNP
          from N100_TEST_MP a """ ,sql_data)
df = db.get_data('SELECT * FROM N100_TEST_MNP',sql_data)

