import os
import pandas as pd
import os
import csv
import datetime


# Folder containing CSV files
csv_dir = '../data'
# Folder containing Split files
split_dir =  '../data_split'

#Reading a config file to set chunk size
fd1 = open("chunk_size.txt", 'r')
chunk_config = int(fd1.read())
chunk_config

#log start time
start_exec_time = datetime.datetime.now()

print('Started')

print('Python : breaking of files started at', start_exec_time)

# Function to split CSV files into chunks
def split_csv(file_path, chunk_size = chunk_config):
    file_name = os.path.basename(file_path)
    df = pd.read_csv(file_path)
    total_records = len(df)
    chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]


    print(f"Total records in '{file_name}': {total_records}")
    for i, chunk in enumerate(chunks):
        ##chunk_file_name = f"{file_name}_chunk_{i + 1}.csv"
        chunk_file_name = f"{os.path.splitext(file_name)[0]}_chunk_{i + 1}.csv"
        chunk.to_csv(os.path.join(split_dir, chunk_file_name), index=False)
        print(f"Chunked file '{chunk_file_name}' created with {len(chunk)} records.")



    #print(f"Total records in '{file_name}': {total_records}")

# Loop through CSV files in the folder and split them into chunks
for file_name in os.listdir(csv_dir):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_dir, file_name)
        split_csv(file_path)

#log end
end_exec_time = datetime.datetime.now()
print('Python : breaking of files ended at', end_exec_time)
print('Completed')

