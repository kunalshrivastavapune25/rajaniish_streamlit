import sqlite3 as sq
import pandas as pd

def get_data(user_query,sql_data = 'C:\\NSE\\SA.sqlite2'):
    #sql_data = 'C:\\NSE\\SA.sqlite2' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    ret_df = pd.read_sql_query(user_query, conn)
    conn.close()
    return ret_df

def insert_data(table_name,df,sql_data = 'C:\\NSE\\SA.sqlite2'):
    #sql_data = 'C:\\NSE\\SA.sqlite2' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    c = conn.cursor()  
    c.execute('DROP TABLE IF EXISTS ' + table_name + '_TEMP' )
    df.to_sql(table_name + '_TEMP', conn , if_exists='replace', index=True) # - writes the pd.df to SQLIte DB
    c.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' AS select * from ' + table_name + '_TEMP where 1=2'   )
    c.execute('insert into ' + table_name + ' select * from ' + table_name + '_TEMP'   )
    conn.commit()
    conn.close()
 
    
def resample_tabs(sql_data = 'C:\\NSE\\SA.sqlite2'):
    #sql_data = 'C:\\NSE\\SA.sqlite2' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    c = conn.cursor()  
    # Read the script file
    with open('CreateTables.sql', 'r') as file:
        script = file.read()
    c.executescript(script)
    conn.commit()
    conn.close()

    
def drop_data(table_name,sql_data = 'C:\\NSE\\SA.sqlite2'):
    #sql_data = 'C:\\NSE\\SA.sqlite2' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    c = conn.cursor()  
    c.execute('DROP TABLE IF EXISTS ' + table_name  )
    conn.commit()
    conn.close()
    
def execute_qry(qry,sql_data = 'C:\\NSE\\SA.sqlite2'):
    #sql_data = 'C:\\NSE\\SA.sqlite2' #- Creates DB names SQLite
    conn = sq.connect(sql_data)
    c = conn.cursor()  
    c.execute(qry )
    conn.commit()
    conn.close()    