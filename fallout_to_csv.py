import os
import csv
import cx_Oracle
import datetime
import pandas as pd
from config import oracle_db_con
#from config import wfm_db_con

# Directory containing SQL scripts
sql_dir = '../fallout_src'
csv_dir = '../data/fallout_data'

#logging status of each csv.
csv_logging='program_name,program_location,program_start_time,program_end_time,executed_by,file_name,num_record_errors,num_record_warnings,program_status'
program_name='CSV_GENERATION'
program_location='/apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin'
time =  datetime.datetime.now()
print('Python : Extraction of csv from fallout sql started at', time)
# Connect to the database
# dsn = cx_Oracle.makedsn(oracle_db_con.db_host, oracle_db_con.db_port, service_name=oracle_db_con.db_service)
# conn = cx_Oracle.connect(oracle_db_con.db_user, oracle_db_con.db_password, dsn=dsn)

#log total execution time
start_exec_time = datetime.datetime.now()

fd1 = open("clli_config_sql.txt", 'r')
cllis_config = fd1.read()
for filename in os.listdir(sql_dir):
    if filename.endswith('mr_ac_services_fallouts.sql'):
        # Read the SQL script
        print(filename)
        with open(os.path.join(sql_dir, filename), 'r') as f:
            sql = f.read()

            sql = sql.replace('#variable',cllis_config)
           # print(sql)
            startTime_files = datetime.datetime.now()
            print('Starting  extraction for files '+ filename, startTime_files)
            csv_logging= csv_logging + '\n'+program_name+','+program_location+','+startTime_files.strftime("%Y-%m-%d %I:%M:%S")
        try:
            if filename in ['mr_site_resource.sql']:
                #print('wfm')
                db_user = oracle_db_con.db_user_wfm
                db_host = oracle_db_con.db_host_wfm
                db_port = oracle_db_con.db_port_wfm
                db_service = oracle_db_con.db_service_wfm
                db_password = oracle_db_con.db_password_wfm
                sql = sql.replace("@wfm_link","")
            else:
               # print('pims')

                db_user = oracle_db_con.db_user
                db_host = oracle_db_con.db_host
                db_port = oracle_db_con.db_port
                db_service = oracle_db_con.db_service
                db_password = oracle_db_con.db_password
                #print(db_user,db_password)


            # Connect to the database
            dsn = cx_Oracle.makedsn(db_host, db_port, service_name=db_service)
            conn = cx_Oracle.connect(db_user,db_password, dsn=dsn)

            # Execute the SQL query
            cursor = conn.cursor()
            cursor.execute(sql)

            # Extract the results to a CSV file
            csv_filename = csv_dir + "/" + filename.replace('.sql', '.csv')
            with open(csv_filename, 'w',encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([col[0] for col in cursor.description])
                for row in cursor:
                    writer.writerow(row)

            # Close the cursor
            #cursor.close()
            startTime_files = datetime.datetime.now()
            print('Extraction completed for file  '+ filename, startTime_files)
            results =  pd.read_csv(csv_filename,encoding='utf-8', engine='python')
            print("Records fetched of file " +filename+" is "+ str(len(results)))
            csv_logging= csv_logging+','+startTime_files.strftime("%Y-%m-%d %I:%M:%S")+',automate,'+filename+',0,0'
            csv_logging= csv_logging+',SUCCESS'
        except Exception as e:
            csv_logging= csv_logging+','+startTime_files.strftime("%Y-%m-%d %I:%M:%S")+',automate,'+filename+',,'
            csv_logging= csv_logging+',FAILED'
            print(e)
        finally:
            # Close the cursor
            cursor.close()
            # Close the database connection
            conn.close()


# Close the database connection
end_exec_time = datetime.datetime.now()
#conn.close()
print('Python : Extraction of csv fallout sql ended at ', startTime_files)
print('_____________________________________________________________________________________')
print('Log: process started at ', start_exec_time,' and finished at ',end_exec_time)
print('_____________________________________________________________________________________')
count = 0
for path in os.scandir(csv_dir):
    if path.is_file():
        count += 1
print("Total number of files from the extraction are", count)
with open("log/csv_logging_fallout.csv", 'w',encoding='utf-8', newline='') as f:
    f.write(csv_logging)
#print('Loaded status in postgres DB. Please check there.')
#print('_____________________________________________________________________________________')

