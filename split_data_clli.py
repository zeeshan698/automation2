import os
import pandas as pd
import datetime

# input_folder = "C:/Users/AHMSY8R/Downloads/psc/data"
# output_folder = "C:/Users/AHMSY8R/Downloads/psc/data_split_clli"

# Folder containing CSV files
input_folder = '../data'
# Folder containing Split files based on clli
output_folder = '../data_split_clli'


column_name = "Location *"
file_name = "BatteryStrings.csv"

#list of strings to filter 
#Define the list of clli  to filter
clli_filename ='clli_config.txt'

#read site code config file
with open(clli_filename, 'r') as f:
    content = f.read()
values = content.strip().split(',')
filter_list = [value.strip().strip("'") for value in values]
string_to_filter = filter_list

file_path = os.path.join(input_folder, file_name)

#log start time
start_exec_time = datetime.datetime.now()

print('Started')

print('Python : breaking of files started at', start_exec_time)

#read the source csv file
df = pd.read_csv(file_path,encoding='utf-8', engine='python')

#Dictionary to store dataframes for each clli
filtered_dfs = {}

#Dictionary to store count of records
record_count_dict = {}

#Iterate through each clli, filter dataframe and store in the dictionary
for string in string_to_filter:
    filtered_dfs[string] = df[df[column_name].str.contains(string,case = False)]
    record_count = len(filtered_dfs[string])
    record_count_dict[string] = record_count
    
#record count for each clli broken file
    record_count = len(filtered_dfs)
    
#export each dataframe/clli to individual csv files
for string,filtered_df in filtered_dfs.items():
    #filename =   f'BatteryStrings_{string}.csv'
    filename =  os.path.join(output_folder, f'BatteryStrings_{string}.csv')
    filtered_df.to_csv(filename,index= False)     

# Save the merged data to a new CSV file
      
print("Records  in original BatteryStrings.csv file  is",  str(len(df)))

# print record for each clli broken file
for string,count in record_count_dict.items():
    print(f"Records  in BatteryStrings_{string}.csv is {count}")
    
#log end 
end_exec_time = datetime.datetime.now()
print('Python : breaking of files ended at', end_exec_time)    
print('Completed')    
