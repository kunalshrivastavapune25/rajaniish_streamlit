import pandas as pd
import Database as db
import streamlit as st
import base64
import copy

def get_download_link(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}">Download Excel File</a>'
    return href

    



st.set_page_config(layout="wide")
col1, col2 = st.columns(2)
try:
    
    if st.session_state["authentication_status"]:
        with st.expander("ChartInk_Tested_1D-15M"):
            st.markdown('##### Chartink Csv Details')
            dis = False
            col1, col2  = st.columns([2, 8]) 
            with col1:
                stock_type_T = st.selectbox("Select Stock Type", [ "100","INDEX"] , key='v')
        
            with col2:
                st.markdown('##### Select Interval')
                interval_T = st.radio("Interval", ['1D' , '1H', '15M', '5M'],key='w')

                
                


            
            entry_uploaded_file = st.file_uploader("Choose a entryPoint CSV file", type="csv", key='e')
            if entry_uploaded_file is not None:
                entry_data = pd.read_csv(entry_uploaded_file)
                
            target_uploaded_file = st.file_uploader("Choose a exitPoint CSV file", type="csv",key='t' )
            if target_uploaded_file is not None:
                target_data = pd.read_csv(target_uploaded_file)

                
            #col1, col2,col3, col4  = st.columns([2, 2, 2, 2]) 
            #with col1:
            #    risk = st.text_input(label="Risk Pct",value="5" ,key=34)        
            #with col2:
            #    rewards = st.text_input(label="Reward Pct",value="15" ,key=35)
                
                

            
            if st.button('Start Analysis', help="red",key='ff'):    
                if target_uploaded_file is None:
                    target_data =  copy.deepcopy(entry_data) 
                writer = pd.ExcelWriter('Analysis_Sheet.xlsx', engine='xlsxwriter')
                entry_data.to_excel(writer, sheet_name='entryPoint CSV file', index=False)
                
                src_db = 'C:\\NSE\\SA.sqliteDB_NIFTY' + stock_type_T +'_' + interval_T
                st.write(src_db)                      
                main_tab = 'N' + stock_type_T + '_OHLC_'+ interval_T
                main_tab_df = db.get_data('select * from ' + main_tab,src_db)    
                entry_data_tab_name = 'ENTRY_TAB'
                target_data_tab_name = 'EXIT_TAB'
                
                username = st.session_state["name"]
                usr_db = 'C:\\NSE\\SA.sqlite' + username
                st.write(usr_db)  

                db.drop_data(main_tab,usr_db)
                db.insert_data(main_tab, main_tab_df,usr_db )  
                st.success(main_tab + ' Created !!')            

                db.drop_data(entry_data_tab_name,usr_db)
                db.insert_data(entry_data_tab_name, entry_data,usr_db )  
                st.success(entry_data_tab_name + ' Created !!')            

                db.drop_data(target_data_tab_name,usr_db)
                db.insert_data(target_data_tab_name, target_data,usr_db )  
                st.success(target_data_tab_name + ' Created !!') 
                
                
                    
                
                
                
                db.execute_qry("""update entry_tab set date = 
    replace(CASE
        WHEN date LIKE '%-%-% % %m'
            THEN
                SUBSTR(date, 7, 4) || '-' ||  -- Extract year
                SUBSTR(date, 4, 2) || '-' ||  -- Extract day
                SUBSTR(date, 1, 2) || ' ' ||  -- Extract month
                CASE
                    WHEN date LIKE '% pm' and cast(SUBSTR(date, 12, 2) AS INTEGER) <> 12
                        THEN
                            CAST((CAST(SUBSTR(date, 12, 2) AS INTEGER) + 12) AS TEXT) || ':' ||  -- Convert hour to 24-hour format
                            SUBSTR(date, instr('01-04-2024 2:15 pm',':') +1, 2) || ':00'
                    ELSE
                        SUBSTR(date, 12, 5) || ':00'
                END
        ELSE
                SUBSTR(date, 7, 4) || '-' ||  -- Extract year
                SUBSTR(date, 4, 2) || '-' ||  -- Extract day
                SUBSTR(date, 1, 2)   -- Extract month
    END,' :',':')	 """,usr_db)

                target_data_tab_name = 'EXIT_TAB'
                
                db.drop_data(target_data_tab_name,usr_db)
                db.insert_data(target_data_tab_name, target_data,usr_db )  
                st.success(target_data_tab_name + ' Created !!')           
                db.execute_qry("""update exit_tab set date = 
    replace(CASE
        WHEN date LIKE '%-%-% % %m'
            THEN
                SUBSTR(date, 7, 4) || '-' ||  -- Extract year
                SUBSTR(date, 4, 2) || '-' ||  -- Extract day
                SUBSTR(date, 1, 2) || ' ' ||  -- Extract month
                CASE
                    WHEN date LIKE '% pm' and cast(SUBSTR(date, 12, 2) AS INTEGER) <> 12
                        THEN
                            CAST((CAST(SUBSTR(date, 12, 2) AS INTEGER) + 12) AS TEXT) || ':' ||  -- Convert hour to 24-hour format
                            SUBSTR(date, instr('01-04-2024 2:15 pm',':') +1, 2) || ':00'
                    ELSE
                        SUBSTR(date, 12, 5) || ':00'
                END
        ELSE
                SUBSTR(date, 7, 4) || '-' ||  -- Extract year
                SUBSTR(date, 4, 2) || '-' ||  -- Extract day
                SUBSTR(date, 1, 2)   -- Extract month
    END,' :',':')	 """,usr_db)
    
    
                if interval_T in ( '1H', '15M', '5M'):
                    db.execute_qry("""update entry_tab set date = 
        date || 'T09:15:00' where  date not LIKE '%:%' """,usr_db)
                    db.execute_qry("""update exit_tab set date = 
        date || 'T09:15:00' where  date not LIKE '%:%'   """,usr_db)    

                db.create_index("I2",target_data_tab_name,"date(date)",usr_db)
                
                
                db.create_index("I1",entry_data_tab_name,"date(date)",usr_db)
                db.create_index("I4",main_tab,"date(datetime)",usr_db)
                db.create_index("I5",main_tab,"ticker",usr_db)
                db.create_index("I6",main_tab,"ticker , date(datetime) ",usr_db)

                db.execute_qry("""delete from """ + main_tab + """ where ticker not in (
                select symbol from Exit_TAB 
                union 
                select symbol  from Entry_TAB)   """,usr_db)  




                if target_uploaded_file is not None:
                    target_data.to_excel(writer, sheet_name='exitPoint CSV file', index=False)
                    db.drop_data(entry_data_tab_name + '_HD',usr_db)
                    df = db.get_data("""select a.*, 
                    (select min(date(b.date)) from """ + target_data_tab_name + """ b 
                     where a.symbol = b.symbol and date(b.date) > date(a.date)) hit_date
                    from """ + entry_data_tab_name + """ a""",usr_db)
                    db.insert_data(entry_data_tab_name + '_HD', df,usr_db )  
                    st.write("""select a.*, 
                    (select min(date(b.date)) from """ + target_data_tab_name + """ b 
                     where a.symbol = b.symbol and date(b.date) > date(a.date)) hit_date
                    from """ + entry_data_tab_name + """ a""")
                    st.write(df)
                    st.success(entry_data_tab_name + '_HD' + ' Created !!')            
    
    
                    db.create_index("I3",entry_data_tab_name + '_HD',"date(date)",usr_db)
              
                    
                    db.drop_data(entry_data_tab_name + '_EP',usr_db)
                    df = db.get_data("""select a.*, 
                    (select b.close 
                    from """ + main_tab + """ b 
                    where a.symbol = b.ticker 
                    and date(b.datetime) = date(a.date) ) ep
                    from """ + entry_data_tab_name + """_hd a""",usr_db)
                    db.insert_data(entry_data_tab_name + '_EP', df,usr_db )  
                    st.write("""select a.*, 
                    (select b.close 
                    from """ + main_tab + """ b 
                    where a.symbol = b.ticker 
                    and date(b.datetime) = date(a.date) ) ep
                    from """ + entry_data_tab_name + """_hd a""")
                    st.write(df)
                    st.success(entry_data_tab_name + '_EP' + ' Created !!')            
    
                    db.create_index("I7",entry_data_tab_name + '_EP',"symbol , date(date) ",usr_db)
                    db.create_index("I8",entry_data_tab_name + '_EP',"date(date) ",usr_db)
    
                    db.drop_data(entry_data_tab_name + '_HP',usr_db)
                    df = db.get_data("""select a.*, 
                    (select b.close 
                    from """ + main_tab + """ b 
                    where a.symbol = b.ticker 
                    and date(b.datetime) = date(a.hit_date) ) hp
                    from """ + entry_data_tab_name + """_ep a""",usr_db)
                    db.insert_data(entry_data_tab_name + '_HP', df,usr_db )  
                    st.write("""select a.*, 
                    (select b.close 
                    from """ + main_tab + """ b 
                    where a.symbol = b.ticker 
                    and date(b.datetime) = date(a.hit_date) ) hp
                    from """ + entry_data_tab_name + """_ep a""")
                    st.write(df)
                    st.success(entry_data_tab_name + '_HP' + ' Created !!')            
    
    
    
                    db.drop_data(entry_data_tab_name + '_MAXP',usr_db)
                    df = db.get_data("""select a.*, 
                    (select max(b.close) 
                    from """ + main_tab + """ b 
                    where a.symbol = b.ticker 
                    and date(b.datetime) between date(a.date) and date(a.hit_date) ) maxp
                    from """ + entry_data_tab_name + """_hp a""",usr_db)
                    db.insert_data(entry_data_tab_name + '_MAXP', df,usr_db )  
                    st.write("""select a.*, 
                    (select max(b.close) 
                    from """ + main_tab + """ b 
                    where a.symbol = b.ticker 
                    and date(b.datetime) between date(a.date) and date(a.hit_date) ) maxp
                    from """ + entry_data_tab_name + """_hp a""")
                    st.write(df)
                    st.success(entry_data_tab_name + '_MAXP' + ' Created !!')            
                    
    
                    
                    db.drop_data(entry_data_tab_name + '_MINP',usr_db)
                    df = db.get_data("""select a.*, 
                    (select min(b.close) 
                    from """ + main_tab + """ b 
                    where a.symbol = b.ticker 
                    and date(b.datetime) between date(a.date) and date(a.hit_date) ) minp
                    from """ + entry_data_tab_name + """_maxp a""",usr_db)
                    db.insert_data(entry_data_tab_name + '_MINP', df,usr_db )  
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
                            ))""",usr_db)    
    
                    st.write("""delete  from ENTRY_TAB_MINP where rowid in (
                            select rowid from 
                            ENTRY_TAB_MINP  a
                            where exists(
                            select 1 from ENTRY_TAB_MINP a1 
                            where a.symbol = a1.symbol
                            and date(a1.date) > date(a.date)
                            and  date(a1.date) between date(a.date) and date(a.hit_date)
                            ))""")
                    
                    df = db.get_data("select a.* from " + entry_data_tab_name + "_MINP a",usr_db)
                    df.to_excel(writer, sheet_name='Sheet3', index=False)                
                    
                    db.drop_data(entry_data_tab_name + '_SUMM',usr_db)
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
    group by Symbol""",usr_db)
                    db.insert_data(entry_data_tab_name + '_SUMM', df,usr_db )  
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
                    
                    df = db.get_data("select a.* from " + entry_data_tab_name + "_SUMM a",usr_db)                
                    df.to_excel(writer, sheet_name='Sheet4', index=False)                






                db.drop_data('ENTRY_TAB_P',usr_db)
                df = db.get_data("""select a.*, b.Close, 
(
select max(cast(High as REAL ))  from """ + main_tab + """ b1 
where a.symbol = b1.ticker
and date(substr(a.date,1,10)) = date(substr(b1.datetime,1,10))
and datetime(a.date) < datetime(b1.datetime)

) as max_High,
(
select min(cast(Low as REAL))  from """ + main_tab + """ b1 
where a.symbol = b1.ticker
and date(substr(a.date,1,10)) = date(substr(b1.datetime,1,10))
and datetime(a.date) < datetime(b1.datetime)
) as min_Low
from ENTRY_TAB a,
""" + main_tab + """ b
where a.symbol = b.ticker
and datetime(a.date) = datetime(b.datetime)""",usr_db)
                db.insert_data('ENTRY_TAB_P', df,usr_db )                  

                db.drop_data('ENTRY_TAB_q',usr_db)
                df = db.get_data("""select a.*,
(select min(b1.datetime)  from """ + main_tab + """ b1 
where a.symbol = b1.ticker
and date(substr(a.date,1,10)) = date(substr(b1.datetime,1,10))
and CAST(b1.high AS REAL) = CAST(A.MAX_hIGH AS REAL)
and datetime(a.date) < datetime(b1.datetime)
 ) as max_time,
(select min(b1.datetime)  from """ + main_tab + """ b1 
where a.symbol = b1.ticker
and date(substr(a.date,1,10)) = date(substr(b1.datetime,1,10))
and CAST(b1.lOW AS REAL) = CAST(A.Min_lOW AS REAL)
and datetime(a.date) < datetime(b1.datetime)
 ) as mIN_time,
max_High -  CLOSE AS hmc,
mIN_LOW -  CLOSE AS Lmc
from ENTRY_TAB_P a
""",usr_db)
                db.insert_data('ENTRY_TAB_q', df,usr_db )                     
                df.to_excel(writer, sheet_name='Intra_day_Analysis', index=False)      
                db.drop_data('ENTRY_TAB_r',usr_db)
                df = db.get_data(""" SELECT SYMBOL, count(1) TOTAL_TRADE, MAX(hmc) max_high_MINUS_CLOSE, MIN (Lmc) min_low_minus_close,
avg(hmc) avg_high_MINUS_CLOSE, avg (Lmc) avg_low_minus_close
 FROM ENTRY_TAB_q
 GROUP BY SYMBOL""",usr_db)
                db.insert_data('ENTRY_TAB_r', df,usr_db )                    
                df.to_excel(writer, sheet_name='Intra_day_Analysis_Summary', index=False)                    
                
                
                
                
                
                
                writer.close()    
                st.success("Excel file with multiple tabs created successfully!")
                st.markdown(get_download_link('Analysis_Sheet.xlsx'), unsafe_allow_html=True)




                    
                    
                



    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
except KeyError:
    # If KeyError occurs, display a message to sign in
    st.warning('Please sign in.')