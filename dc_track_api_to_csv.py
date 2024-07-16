import requests
import os
import json
import datetime
from config import api_credentials as ac
import pandas as pd

#API configurations
username = ac.username
password = ac.password
login_url = ac.login_url
host_url = ac.host_url


#directory to read JSON and write CSV
json_dir = '../api_json'
csv_dir = '../dctrack_csv'
site_code_array=[]
clli_filename="clli_config.txt"
site_code_offset=20
site_str=''
split_site_code=[]
i=0

#logging status of each csv.
csv_logging_json='program_name,program_location,program_start_time,program_end_time,executed_by,file_name,num_record_errors,num_record_warnings,program_status'
program_name='CSV_GENERATION_FROM_DC_TRACK_API'
program_location='/apps/opt/application/pscmigration/1pscmigration/scripts/phase1_extract/bin'
time =  datetime.datetime.now()
print('Python : Extraction of csv from json started at', time)


#start execution time
start_exec_time = datetime.datetime.now()

session = requests.Session()
session.auth =  (username,password)

with open(clli_filename, 'r') as fclli:
    text=fclli.readline()
    while text != "":
        site_code_array.append(text.replace("'","").replace("\n","").replace(",",""))
        text = fclli.readline()
        #print(text.replace("'","").replace("\n","").replace(",",""))
#print(site_code_array)
#Create chunk of site codes
for name in site_code_array:
    if i == 0:
        site_str = name
    else:
        site_str = site_str + " OR " + name
    i = i + 1
    if i == site_code_offset:
        split_site_code.append(site_str)
        i=0
        site_str=''
if i > 0 and i < site_code_offset:
    split_site_code.append(site_str)
    i=0
    site_str=''


#Read json files from directory
i = 0
for site_code in split_site_code:
    i = int(i) + 1
    for file_name in os.listdir(json_dir):
        #print("Name of JSON file ",file_name)


        try:
            startTime_files = datetime.datetime.now()
            print(f"started fetching CSV for JSON file {file_name} at {datetime.datetime.now()}")
            csv_logging_json= csv_logging_json + '\n'+program_name+','+program_location+','+startTime_files.strftime("%Y-%m-%d %I:%M:%S")

            #Read contents of JSON files
            with open(os.path.join(json_dir, file_name), 'r') as f:
                #print(f.read().replace("true","True").replace("false","False"))
                todo = eval(f.read().replace("true","True").replace("false","False"))
                #print(todo["columnFilter"]["columns"])
                for x in todo["columnFilter"]["columns"]:
                    if x["name"] == "tiLocationName":
                        if "contains" in  x["filter"]:
                            #x["filter"]["contains"] = " OR ".join(site_code_array)
                            x["filter"]["contains"] = site_code
                            #print(x["filter"]["contains"])
                # or json.loads(f.read())
               # print(todo)
                # Send a post request to the login page to get any required cookies or CSRF tokens
                response = session.post(login_url,json = todo)
                #print(response.text)
                if response.status_code == 200:
                    print("success")
                    #print(response.json()['url'])
                    URL = f"{host_url}{response.json()['url']}"
                    # 2. download the data behind the URL
                    response_csv = requests.get(URL)
                    json_csv= file_name.split(".")[0]+"_"+ str(i) +".csv"
                    #print(response.text)
                    #json_csv=file_name.split(".")[0]+".csv"
                    with open(f"{csv_dir}/{json_csv}", 'w',encoding='utf-8', newline='') as f:
                        f.write(response_csv.text)
                    startTime_files = datetime.datetime.now()
                    print(f"finished fetching CSV for JSON file {file_name} at {datetime.datetime.now()}")
                    results =  pd.read_csv(f"{csv_dir}/{json_csv}",encoding='utf-8', engine='python')
                    print("Records fetched of file " +json_csv+" is "+ str(len(results)))
                    csv_logging_json= csv_logging_json+','+startTime_files.strftime("%Y-%m-%d %I:%M:%S")+',automate,'+json_csv+',0,0'
                    csv_logging_json= csv_logging_json+',SUCCESS'
                else:
                    print("failed")
                    print(f"Failed fetching CSV for JSON file {file_name}")
                    print(response.json()['url'])
        except Exception as e:
            print(f"Error occurred in json file {file_name}")
            csv_logging_json= csv_logging_json+','+startTime_files.strftime("%Y-%m-%d %I:%M:%S")+',automate,'+json_csv+',,'
            csv_logging_json= csv_logging_json+',FAILED'
            #print(f"JSON Data is  {json.dumps(todo)}")
            print("Error-",e)


#end execution time
end_exec_time = datetime.datetime.now()
print(f"Ended fetching CSV for JSON file {file_name} at {datetime.datetime.now()}")
print('_____________________________________________________________________________________')
print('API to CSV: Process started at ', start_exec_time,' and finished at ',end_exec_time)
print('_____________________________________________________________________________________')
with open("log/csv_logging_json.csv", 'w',encoding='utf-8', newline='') as f:
    f.write(csv_logging_json)

