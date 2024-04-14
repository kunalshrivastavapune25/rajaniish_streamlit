import pandas as pd
import Database as db
import streamlit as st
import base64

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
                
            target_uploaded_file = st.file_uploader("Choose a exitPoint CSV file", type="csv",key='t',disabled= (interval_T == '15M') )
            if target_uploaded_file is not None:
                target_data = pd.read_csv(target_uploaded_file)    

            col1, col2,col3, col4  = st.columns([2, 2, 2, 2]) 
            with col1:
                risk = st.text_input(label="Risk Pct",value="5" ,key=34)        
            with col2:
                rewards = st.text_input(label="Reward Pct",value="15" ,key=35)
                
                

            
            if st.button('Start Analysis', help="red",key='ff'):    
                writer = pd.ExcelWriter('multi_tab_excel.xlsx', engine='xlsxwriter')
                entry_data.to_excel(writer, sheet_name='Sheet1', index=False)
                
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
case when date  like '__-__-____' then 
 substr(date,7,4) 
    || '-' || 
    substr(date,4,2) 
    || '-' || 
    substr(date,1,2) 
    || 
    case when substr(date,11,15) <> '' then '-' || substr(date,11,15) else '' end
else 
	substr(date,7,4) 
|| '-' || 
substr(date,4,2) 
|| '-' || 
substr(date,1,2) 
|| 
case when substr(date,11,15) <> '' then ' ' 
|| case when cast(substr(date,12,2) as int) in (1,2,3,4,5) then cast(substr(date,12,2) as int) + 12 else substr(date,12,2) end   || ':' || substr(date,15,2) || ':00' else '' end
end	 """,usr_db)

                target_data_tab_name = 'EXIT_TAB'
                target_data.to_excel(writer, sheet_name='Sheet2', index=False)
                db.drop_data(target_data_tab_name,usr_db)
                db.insert_data(target_data_tab_name, target_data,usr_db )  
                st.success(target_data_tab_name + ' Created !!')           
                db.execute_qry("""update exit_tab set date = 
case when date  like '__-__-____' then 
 substr(date,7,4) 
    || '-' || 
    substr(date,4,2) 
    || '-' || 
    substr(date,1,2) 
    || 
    case when substr(date,11,15) <> '' then '-' || substr(date,11,15) else '' end
else 
	substr(date,7,4) 
|| '-' || 
substr(date,4,2) 
|| '-' || 
substr(date,1,2) 
|| 
case when substr(date,11,15) <> '' then ' ' 
|| case when cast(substr(date,12,2) as int) in (1,2,3,4,5) then cast(substr(date,12,2) as int) + 12 else substr(date,12,2) end   || ':' || substr(date,15,2) || ':00' else '' end
end	 """,usr_db)
                db.create_index("I2",target_data_tab_name,"date(date)",usr_db)
                
                
                db.create_index("I1",entry_data_tab_name,"date(date)",usr_db)


                    
                    
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