import os
import pandas as pd
import datetime
import psycopg2
from config import postgres_db_con

conn = psycopg2.connect(database = postgres_db_con.database,user = postgres_db_con.user, password= postgres_db_con.password,host = postgres_db_con.host, port = postgres_db_con.port)
conn.autocommit = True
cursor = conn.cursor()

#Directory where csv stored.
csv_dir = '../data/premigration_data'

#log variables
csv_log="program_name,program_function,program_run_date,program_end_date,source_record_cnt,error_record_cnt,target_record_cnt"
program_name='pythonCode'
program_function='import_postgres_premigration'
program_run_date=''
program_end_date=''
postgres_columns_names = ''

with open('postgres_premigration_import_cofig.txt', 'r') as f:
    startTime_files = datetime.datetime.now()
    program_run_date=startTime_files.strftime("%Y-%m-%d %I:%M:%S")
    text=f.readline()
    while text !="":
        #print(text)

        row=text.split(",")
        tab_name=row[0]
        csv_file_name=row[1].replace("\n","")
        print(tab_name+","+csv_file_name)
        program_name = csv_file_name
        csv_log=csv_log + "\n" + program_name+","+program_function+","+program_run_date

        # pull column names
        pd_cols=pd.read_csv(csv_dir +"/"+ csv_file_name,encoding='utf-8', engine='python')
        columns = pd_cols.columns.tolist()
        postgres_columns_names = '"'+'","'.join (columns)+'"'

        # read csv file to get counts as csv_f:
        pd1=pd.read_csv(csv_dir +"/"+ csv_file_name,encoding='utf-8', engine='python')
        source_record_cnt=len(pd1)
        print(f"No of Records in csv file {csv_file_name} is {source_record_cnt}")
        #truncate table
        sql=f"delete from {tab_name}"
        #print(sql)
        cursor.execute(sql)
        #load data into postgres db
        sql = f'''COPY {tab_name}({postgres_columns_names}) FROM '/apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/data/premigration_data/{csv_file_name}' delimiter ',' csv header;'''
        #print(sql)
        cursor.execute(sql)
        #read counts
        sql=f"select count(*) from {tab_name}"
        #print(sql)
        cursor.execute(sql)
        #fetch data
        rslt=cursor.fetchone()
        #print(rslt[0])
        tab_record_cnt=int(rslt[0])
        print(f"No of Records in table {tab_name} is {tab_record_cnt}")
        startTime_files = datetime.datetime.now()
        program_end_date=startTime_files.strftime("%Y-%m-%d %I:%M:%S")
        csv_log=csv_log +","+program_end_date +","+str(source_record_cnt)+",0,"+str(tab_record_cnt)

        text=f.readline()
#print(csv_log)
with open("log/csv_premigration_import_to_postgres.csv", 'w',encoding='utf-8', newline='') as f:
    f.write(csv_log)

# Close the database connection
conn.close()

