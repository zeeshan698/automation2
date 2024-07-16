import requests
import os
import json
import datetime
from config import api_credentials_permissions as ac

#API configurations
username = ac.username
password = ac.password
login_url = ac.login_url
perm_url = ac.permission_url
host_url = ac.host_url


#directory to read JSON and write CSV
json_dir = '../api_permission'
site_code_array=[]
clli_filename="clli_config.txt"
entityId=0
site_index=1

#start execution time
start_exec_time = datetime.datetime.now()

time =  datetime.datetime.now()
print('Python : Permission process started at ', time)

#Site JSON
session = requests.Session()
session.auth =  (username,password)
#Permission JSON
session_pr = requests.Session()
session_pr.auth =  (username,password)

#read all site codes and load into array
with open(clli_filename, 'r') as fclli:
    text=fclli.readline()
    while text != "":
        site_code_array.append(text.replace("'","").replace("\n","").replace(",",""))
        text = fclli.readline()

#print(site_code_array)
#Read Each site code to generate ID and permissions
for site_code in site_code_array:
    #read Site json file
    print(f"{site_index}. started for site {site_code}")
    site_index=site_index+1
    print("---------------------------------")
    with open(os.path.join(json_dir, "Site.json"), 'r') as f:
        site_json_data = eval(f.read().replace("true","True").replace("false","False"))
        site_json_data["columns"][0]["filter"]["contains"]=site_code
        #print(json.dumps(site_json_data))
        try:
            print("Initiated site_json call.")
            # Send a post request to the login page to get any required cookies or CSRF tokens
            response = session.post(login_url,json = site_json_data)
            #print(response.text)
            site_json_res=response.json()
            if response.status_code == 200:
                #print(site_json_res["searchResults"][0]["id"])
                print(f"success from Site.json response for site {site_code}")
                #Extract data here for id.
                entityId=0
                if len(site_json_res["searchResults"]) > 0:
                    entityId=site_json_res["searchResults"][0]["id"]
                else:
                    print(f"EntityID is missing for Site.json response for site {site_code}")
            else:
                print("Failed to read response from Site.json for site {site_code}")
        except Exception as e:
            entityId=0
            print(f"Error in Site.json response. {json.dumps(site_json_data)}")

    #read set permission json file
    if entityId > 0:
        print("Initiated Set_permission.json call.")
        with open(os.path.join(json_dir, "Set_Permissions.json"), 'r') as pf:
            perms_json=eval(pf.read().replace("true","True").replace("false","False"))
            for ind in range(len(perms_json["bodies"])):
                perms_json["bodies"][ind]["entityId"]=entityId
            #print(perms_json)
            #Process now
            try:
                # Send a post request to the login page to get any required cookies or CSRF tokens
                response = session_pr.post(perm_url,json = perms_json)
                perms_json_res=response.text
                if response.status_code == 200:
                    print("success from Set_Permissions.json response")
                    #Extract data
                    print(f"Final response for site {site_code} and entityID {entityId} is below-")
                    #print(response.text)
                else:
                    print("Failed to read response from Set_Permissions.json")

            except Exception as e:
                print(f"Error in Set_Permissions response. {json.dumps(perms_json)}")

    else:
        print(f"response for site {site_code} from Site.json not received!")


#end execution time
end_exec_time = datetime.datetime.now()
#conn.close()
print('Python : Permission process ended at ', end_exec_time)
print('_____________________________________________________________________________________')
print('API to Permissions: Process started at ', start_exec_time,' and finished at ',end_exec_time)
print('_____________________________________________________________________________________')

