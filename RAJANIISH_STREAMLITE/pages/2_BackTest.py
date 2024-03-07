import numpy as np
import pandas as pd
import Database as db
import pandas_ta as pt
import streamlit as st
import base64

def get_download_link(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}">Download Excel File</a>'
    return href

def update_status(progress):
    status_bar.progress(progress)
    
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
def BollBnd(DF,n,std):
    "function to calculate Bollinger Band"
    df = DF.copy()
    df["MA"] = df['Close'].rolling(n).mean()
    df["BB_up"] = df["MA"] + std  * df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_dn"] = df["MA"] -  std * df['Close'].rolling(n).std(ddof=0) #ddof=0 is required since we want to take the standard deviation of the population and not sample
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    #df.dropna(inplace=True)
    return df


st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
try:
    
    if st.session_state["authentication_status"]:
        with st.expander("Work In Progress"):
            #st.markdown('#### Chartlink Data Analysis')
            #st.divider()
            st.markdown('##### Chartink Csv Details')
            col1, col2  = st.columns([2, 8]) 
            with col1:
                stock_type = st.selectbox("Select Stock Type", [ "100","INDEX"])
            # Upload CSV file
            with col2:
                uploaded_file = st.file_uploader("Choose a CSV file downloaded from ChartInk", type="csv")
                
                if uploaded_file is not None:
                    data = pd.read_csv(uploaded_file)
                    
        
        
            col1, col2, col3  = st.columns(3)
            # Input for Bollinger Bands parameters
            with col1:
                st.markdown('##### Bollinger Bands Parameters')
                bb_param1 = st.text_input("Parameter 1", value='20')
                bb_param2 = st.text_input("Parameter 2", value='2')
        
            with col2:
            # Input for Stochastic parameters
                st.markdown('##### SuperTrend Parameters')
                st_param1 = st.text_input("Parameter 1", value='14')
                st_param2 = st.text_input("Parameter 2", value='3')
        
            with col3:
                st.markdown('##### Select Interval')
                interval = st.radio("Interval", ['1D' , '1H', '15M'])
                
        
        
            st.markdown('#### Target Logic')
            col1, col2, col3 = st.columns(3)
            with col1:    
                # First set of radio buttons
        
                target_type = st.radio("Price", ['Open', 'High', 'Low', 'Close'])
        
            with col2:
            # Second set of radio buttons
        
                comparison_type = st.radio("Comparison", ["Less Than", "Greater Than"])
                
     
            with col3:
            # Third set of radio buttons
                indicator_type = st.radio("Indicator", ['BBUP', 'BBDOWN', 'ST'])
            diabled = True
            comparison_type1 = "<"
            cond = "cast(b.ST as float) > cast(b.close as float)"
            username = st.session_state["name"]
            if st.button('Confirm', help="red"):
                if comparison_type == "less Than":
                    comparison_type1 = "<"
                if comparison_type == "Greater Than":
                    comparison_type1 = ">"            
                
                cond = st.text_input("Target Conditions", value= ' cast(b.' + target_type + ' as float) ' + comparison_type1 + ' cast(b.' + indicator_type + ' as float) '  )
                ind_params = st.text_input("Indicators", value= 'ST : ' + st_param1 + ',' + st_param2 + ' ; BB : ' + bb_param1 + ',' + bb_param2 )
                username = st.session_state["name"]
                diabled = False
                #cast(b.ST as float) > cast(b.close as float)
                #cast(b.Open as float) > cast(a.BBUP as float) 
            jcond = cond    
            if st.button('Start Analysis', help="red", disabled=diabled):
                if uploaded_file is not None:
                    # Perform some processing here if needed
                    # Generate downloadable file
                    user_tab = 'N' + stock_type + '_TEST'
                    main_tab = 'N' + stock_type + '_OHLC_'+ interval
                    user_main_tab = 'N' + stock_type + '_OHLC_'+ interval + '_FULL'
        
                    
                    sql_data = 'C:\\NSE\\SA.sqlite' + username #- Creates DB names SQLite
                    st.write(sql_data)    
                    db.drop_data(user_tab,sql_data)
                    db.insert_data(user_tab, data,sql_data )
                    st.success('File Uploaded ' + user_tab + ' created')        
                    st.success(user_tab + 'Created !!')
        
                    
                    df = db.get_data('select * from ' + main_tab )
                    df['Datetime'] = pd.to_datetime(df['Datetime'])
                    grouped = df.groupby('ticker')
                    dict_of_dfs = {key: group.reset_index(drop=True) for key, group in grouped}
                    tickers = dict_of_dfs.keys()
        
                    st.success(' Process Started for tickers updation!!')
                    status_bar = st.empty()            
        
                    db.drop_data(user_main_tab,sql_data)
                    count = 0
                    total_tickers = len(tickers)
                    for ticker in tickers:
                        dict_of_dfs[ticker].dropna(inplace=True)
                        
                        count += 1
                        update_status(count / total_tickers)  
                        if len(dict_of_dfs[ticker]) > 50:
                            #st.success('merging for '  + ticker + ' Done!!')
                            
                            df =  dict_of_dfs[ticker]
                            df[['Open', 'High','Low','Close']].astype(float)
                            #dict_of_dfs[ticker]["ST"] =  supertrend(dict_of_dfs[ticker],7,3)
                            dict_of_dfs[ticker]["ST"] = pt.supertrend(df['High'], df['Low'], df['Close'], length= int(st_param1) , multiplier= int(st_param2) )['SUPERT_' + st_param1 + '_' + st_param2 + '.0']
                            dict_of_dfs[ticker]["BBUP"] = BollBnd(dict_of_dfs[ticker],int(bb_param1),int(bb_param2))["BB_up"]
                            dict_of_dfs[ticker]["BBDOWN"] = BollBnd(dict_of_dfs[ticker],int(bb_param1),int(bb_param2))["BB_dn"]
                            #dict_of_dfs[ticker][['lower_band', 'mid', 'upper_band' ]] = pt.bbands(df['Close'], length=20, std=2).iloc[:, :3]
                        #########add column for entry price
                            df =  dict_of_dfs[ticker] 
                            db.insert_data(user_main_tab, df,sql_data )     
                        
             
                    st.success(user_main_tab + ' Created !!')
                    
                    db.drop_data(user_tab + '_EP' ,sql_data)
                    db.execute_qry("create table " + user_tab + """_EP as 
                              select a.*, (select b.close from """ + user_main_tab +  """ b 
                                           where a.symbol = b.ticker 
                                           and date(a.date) = date(b.datetime)) AS EP
                              from """ + user_tab + " a " ,sql_data)
                    df = db.get_data('SELECT * FROM ' + user_tab + '_EP',sql_data)
                    
                    st.success(user_tab + '_EP Created !!')
                    
                    #########add column for hit date
                    
                    db.drop_data(user_tab + '_HD' ,sql_data)
                    db.execute_qry("create table " + user_tab + """_HD as 
                              select a.*, (select MIN(date(b.datetime)) 
                                           from """ + user_main_tab +  """ b 
                                           where a.symbol = b.ticker 
                                           and DATE(a.date) < date(b.datetime) 
                                           and """ + jcond  + """) AS HD
                              from """ + user_tab + "_EP a " ,sql_data)
                    
                    df = db.get_data('SELECT * FROM ' + user_tab + '_HD',sql_data)
                    st.success(user_tab + '_HD Created !!')
                    
                    #########add column for hit price
                    
                    db.drop_data(user_tab + '_HP' ,sql_data)
                    db.execute_qry("create table " + user_tab + """_HP as 
                              select a.*, (select b.close from """ + user_main_tab +  """ b 
                                           where a.symbol = b.ticker 
                                           and date(b.datetime) = date(a.HD) ) AS HP
                              from """ + user_tab + "_HD a " ,sql_data)
                    df = db.get_data('SELECT * FROM ' + user_tab + '_HP',sql_data)
                    
                    st.success(user_tab + '_HP Created !!')
                    
                    #########add column for duration
                    
                    db.drop_data(user_tab + '_D' ,sql_data)
                    db.execute_qry("create table " + user_tab + """_D as 
                              select a.*, julianday(date(HD)) - julianday(date( date)) AS D
                              from """ + user_tab + "_HP a " ,sql_data)
                    df = db.get_data('SELECT * FROM ' + user_tab + '_D',sql_data)
                    st.success(user_tab + '_D Created !!')
                    
                    #########add column for maxprice
                    
                    db.drop_data(user_tab + '_MP' ,sql_data)
                    db.execute_qry("create table " + user_tab + """_MP as 
                              select a.*, (select MAX(b.close) from """ + user_main_tab +  """ b 
                                           where a.symbol = b.ticker 
                                           and  date(b.datetime)  between date(a.date) and date( a.HD)  ) AS MP
                              from """ + user_tab + "_D a " ,sql_data)
                    df = db.get_data('SELECT * FROM ' + user_tab + '_MP',sql_data)
                    st.success(user_tab + '_MP Created !!')
                    
                    #########add column for minprice
                    
                    db.drop_data(user_tab + '_MNP' ,sql_data)
                    db.execute_qry("create table " + user_tab + """_MNP as 
                              select a.*, (select MIN(b.close) from """ + user_main_tab +  """ b 
                                           where a.symbol = b.ticker 
                                           and  date(b.datetime)  between date(a.date) and date( a.HD)) AS MNP
                              from """ + user_tab + "_MP a """ ,sql_data)
                    df = db.get_data('SELECT * FROM ' + user_tab + '_MNP',sql_data)
                    st.success(user_tab + '_MNP Created !!')
                
                #         df =  dict_of_dfs[ticker] 
                #         db.insert_data(table_name, df,sql_data )        
                # Remove the temporary file after download
                #os.remove(temp_file_path)
                    st.write(df)      
                else:
                    st.warning("Please Upload a file first")            
# Run the app
        with st.expander("Temporary"):
            st.markdown('##### Chartink Csv Details')
            col1, col2  = st.columns([2, 8]) 
            with col1:
                stock_type_T = st.selectbox("Select Stock Type", [ "100","INDEX"] , key='v')
        
            with col2:
                st.markdown('##### Select Interval')
                interval_T = st.radio("Interval", ['1D' , '1H', '15M'],key='w')



            
            entry_uploaded_file = st.file_uploader("Choose a entryPoint CSV file", type="csv", key='e')
            if entry_uploaded_file is not None:
                entry_data = pd.read_csv(entry_uploaded_file)
            target_uploaded_file = st.file_uploader("Choose a exitPoint CSV file", type="csv",key='t')
            if target_uploaded_file is not None:
                target_data = pd.read_csv(target_uploaded_file)    
                
            
            
            
            if st.button('Start Analysis', help="red",key='ff'):    
                writer = pd.ExcelWriter('multi_tab_excel.xlsx', engine='xlsxwriter')
                entry_data.to_excel(writer, sheet_name='Sheet1', index=False)
                target_data.to_excel(writer, sheet_name='Sheet2', index=False)

                # entry_data = pd.read_csv ('C:\\Users\\kush0221\\Downloads\\entry.csv')
                # target_data = pd.read_csv ('C:\\Users\\kush0221\\Downloads\\exit_bb.csv')

#                main_tab = 'N100_OHLC_1D'
                main_tab = 'N' + stock_type_T + '_OHLC_'+ interval_T
                main_tab_df = db.get_data('select * from ' + main_tab)    
                entry_data_tab_name = 'ENTRY_TAB'
                target_data_tab_name = 'EXIT_TAB'
                #username = 'anand'
                username = st.session_state["name"]
                
                sql_data = 'C:\\NSE\\SA.sqlite' + username #- Creates DB names SQLite
                st.write(sql_data)  
                
                db.drop_data(main_tab,sql_data)
                db.insert_data(main_tab, main_tab_df,sql_data )  
                st.success(main_tab + ' Created !!')            

                db.drop_data(entry_data_tab_name,sql_data)
                db.insert_data(entry_data_tab_name, entry_data,sql_data )  
                st.success(entry_data_tab_name + ' Created !!')            

                db.drop_data(target_data_tab_name,sql_data)
                db.insert_data(target_data_tab_name, target_data,sql_data )  
                st.success(target_data_tab_name + ' Created !!')            
                
                db.execute_qry("""update entry_tab set date = 
substr(date,7,4) 
|| '-' || 
substr(date,4,2) 
|| '-' || 
substr(date,1,2) 
|| 
case when substr(date,11,15) <> '' then '-' || substr(date,11,15) else '' end """,sql_data)

                db.execute_qry("""update exit_tab set date = 
substr(date,7,4) 
|| '-' || 
substr(date,4,2) 
|| '-' || 
substr(date,1,2) 
|| 
case when substr(date,11,15) <> '' then '-' || substr(date,11,15) else '' end """,sql_data)

                
                db.create_index("I1",entry_data_tab_name,"date(date)",sql_data)
                db.create_index("I2",target_data_tab_name,"date(date)",sql_data)
                
                db.drop_data(entry_data_tab_name + '_HD',sql_data)
                df = db.get_data("""select a.*, 
                (select min(date(b.date)) from """ + target_data_tab_name + """ b 
                 where a.symbol = b.symbol and date(b.date) > date(a.date)) hit_date
                from """ + entry_data_tab_name + """ a""",sql_data)
                db.insert_data(entry_data_tab_name + '_HD', df,sql_data )  
                st.write("""select a.*, 
                (select min(date(b.date)) from """ + target_data_tab_name + """ b 
                 where a.symbol = b.symbol and date(b.date) > date(a.date)) hit_date
                from """ + entry_data_tab_name + """ a""")
                st.write(df)
                st.success(entry_data_tab_name + '_HD' + ' Created !!')            


                db.create_index("I3",entry_data_tab_name + '_HD',"date(date)",sql_data)
                db.create_index("I4",main_tab,"date(datetime)",sql_data)
                db.create_index("I5",main_tab,"ticker",sql_data)
                db.create_index("I6",main_tab,"ticker , date(datetime) ",sql_data)
                
                db.drop_data(entry_data_tab_name + '_EP',sql_data)
                df = db.get_data("""select a.*, 
                (select b.close 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) = date(a.date) ) ep
                from """ + entry_data_tab_name + """_hd a""",sql_data)
                db.insert_data(entry_data_tab_name + '_EP', df,sql_data )  
                st.write("""select a.*, 
                (select b.close 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) = date(a.date) ) ep
                from """ + entry_data_tab_name + """_hd a""")
                st.write(df)
                st.success(entry_data_tab_name + '_EP' + ' Created !!')            

                db.create_index("I7",entry_data_tab_name + '_EP',"symbol , date(date) ",sql_data)
                db.create_index("I8",entry_data_tab_name + '_EP',"date(date) ",sql_data)

                db.drop_data(entry_data_tab_name + '_HP',sql_data)
                df = db.get_data("""select a.*, 
                (select b.close 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) = date(a.hit_date) ) hp
                from """ + entry_data_tab_name + """_ep a""",sql_data)
                db.insert_data(entry_data_tab_name + '_HP', df,sql_data )  
                st.write("""select a.*, 
                (select b.close 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) = date(a.hit_date) ) hp
                from """ + entry_data_tab_name + """_ep a""")
                st.write(df)
                st.success(entry_data_tab_name + '_HP' + ' Created !!')            



                db.drop_data(entry_data_tab_name + '_MAXP',sql_data)
                df = db.get_data("""select a.*, 
                (select max(b.close) 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) between date(a.date) and date(a.hit_date) ) maxp
                from """ + entry_data_tab_name + """_hp a""",sql_data)
                db.insert_data(entry_data_tab_name + '_MAXP', df,sql_data )  
                st.write("""select a.*, 
                (select max(b.close) 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) between date(a.date) and date(a.hit_date) ) maxp
                from """ + entry_data_tab_name + """_hp a""")
                st.write(df)
                st.success(entry_data_tab_name + '_MAXP' + ' Created !!')            
                

                
                db.drop_data(entry_data_tab_name + '_MINP',sql_data)
                df = db.get_data("""select a.*, 
                (select min(b.close) 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) between date(a.date) and date(a.hit_date) ) minp
                from """ + entry_data_tab_name + """_maxp a""",sql_data)
                db.insert_data(entry_data_tab_name + '_MINP', df,sql_data )  
                st.write("""select a.*, 
                (select min(b.close) 
                from """ + main_tab + """ b 
                where a.symbol = b.ticker 
                and date(b.datetime) between date(a.date) and date(a.hit_date) ) minp
                from """ + entry_data_tab_name + """_maxp a""")
                st.write(df)
                st.success(entry_data_tab_name + '_MINP' + ' Created !!')  
                db.execute_qry( """delete  from ENTRY_TAB_MINP where rowid in (
                        select rowid from 
                        ENTRY_TAB_MINP  a
                        where exists(
                        select 1 from ENTRY_TAB_MINP a1 
                        where a.symbol = a1.symbol
                        and date(a1.date) > date(a.date)
                        and  date(a1.date) between date(a.date) and date(a.hit_date)
                        ))""",sql_data)    

                st.write("""delete  from ENTRY_TAB_MINP where rowid in (
                        select rowid from 
                        ENTRY_TAB_MINP  a
                        where exists(
                        select 1 from ENTRY_TAB_MINP a1 
                        where a.symbol = a1.symbol
                        and date(a1.date) > date(a.date)
                        and  date(a1.date) between date(a.date) and date(a.hit_date)
                        ))""")
                
                df = db.get_data("select a.* from " + entry_data_tab_name + "_MINP a",sql_data)
                df.to_excel(writer, sheet_name='Sheet3', index=False)                
                
                db.drop_data(entry_data_tab_name + '_SUMM',sql_data)
                df = db.get_data("""select

Symbol,

min(date) as Trade_Start_Date,

COUNT(1) as Number_of_trades,

round(avg(duration)) Avg_no_of_days_in_trade,

sum(case when pl < 0 then 1 else 0 end ) Loss_Making_Trades,

round(100 * sum(case when pl < 0 then 0 else 1 end ) / COUNT(1)) Profitable_trades_PCT,

julianday(DATE('now') ) -  julianday(min(date)) Total_number_of_days,

round(100* sum(duration) /(julianday(DATE('now') ) -  julianday(min(date)) )) as pct_of_time_capital_was_deployed,

(select first_VALUE(close) OVER (PARTITION BY ticker ORDER BY date(datetime) desc)
from  N100_OHLC_1D c where c.ticker =  b.symbol )
-
(select first_value(ep) OVER (PARTITION BY Symbol ORDER BY date(date)) 
from  ENTRY_TAB_MINP c where c.symbol =  b.symbol )


AS Total_journey_of_stock,
sum(pl) as act_point_cap,
max(pl) max_P,
min(pl) max_L
,
round(100*sum(pl)/(max(hp)-min(ep))) as act_point_cap_pct

from
(select a.*, 
round(hp-ep) as pl,
julianday(hit_date) - julianday(date) as duration
from ENTRY_TAB_MINP a) b
group by Symbol""",sql_data)
                db.insert_data(entry_data_tab_name + '_SUMM', df,sql_data )  
                st.write("""select

Symbol,

min(date) as Trade_Start_Date,

COUNT(1) as Number_of_trades,

round(avg(duration)) Avg_no_of_days_in_trade,

sum(case when pl < 0 then 1 else 0 end ) Loss_Making_Trades,

round(100 * sum(case when pl < 0 then 0 else 1 end ) / COUNT(1)) Profitable_trades_PCT,

julianday(DATE('now') ) -  julianday(min(date)) Total_number_of_days,

round(100* sum(duration) /(julianday(DATE('now') ) -  julianday(min(date)) )) as pct_of_time_capital_was_deployed,

(select first_VALUE(close) OVER (PARTITION BY ticker ORDER BY date(datetime) desc)
from  N100_OHLC_1D c where c.ticker =  b.symbol )
-
(select first_value(ep) OVER (PARTITION BY Symbol ORDER BY date(date)) 
from  ENTRY_TAB_MINP c where c.symbol =  b.symbol )


AS Total_journey_of_stock,
sum(pl) as act_point_cap,
max(pl) max_P,
min(pl) max_L
,
round(100*sum(pl)/(max(hp)-min(ep))) as act_point_cap_pct

from
(select a.*, 
round(hp-ep) as pl,
julianday(hit_date) - julianday(date) as duration
from ENTRY_TAB_MINP a) b
group by Symbol""")
                st.write(df)
                st.success(entry_data_tab_name + '_SUMM' + ' Created !!') 
                
                df = db.get_data("select a.* from " + entry_data_tab_name + "_SUMM a",sql_data)                
                df.to_excel(writer, sheet_name='Sheet4', index=False)                
                
                
                
                
                
                
                
                writer.close()    
                st.success("Excel file with multiple tabs created successfully!")
                st.markdown(get_download_link('multi_tab_excel.xlsx'), unsafe_allow_html=True)






    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
except KeyError:
    # If KeyError occurs, display a message to sign in
    st.warning('Please sign in.')