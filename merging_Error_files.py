import re
import pandas as pd
import os


folder_path = '../Error_file'
# Folder containing Split files
#split_dir =  '../data_split'


# Define the list of file names through config file
Error_filename='Error_file_name_config.txt'
with open(Error_filename, 'r') as f:
    content = f.read()
values = content.strip().split(',')
file_names = [value.strip().strip("'") for value in values]
file_name_input = file_names
res = file_name_input[0]
input_string = res
#pattern = r'^(.*?)_1\.0'
#result = re.search(pattern,input_string)
#extracted_string = result.group(1)
extracted_string  = input_string.split('_')[0]
#output_file_name = f'{extracted_string}.csv'


output_path = f'../Error_file/{extracted_string}.csv'

#file_names  = [Error_file_names ]
#file_names = ['BDFB breaker_1.0fdc2afb-dfb3-4725-b8bd-85ee835f18f2-error.csv', 'BDFB breaker_2.70167732-06a3-470d-a53e-1886a659f00a-error.csv', 'BDFB breaker_3.cd637795-f17e-48e9-8496-ce2efc6a9b3b-error.csv']  # Replace these with your actual file names
merged_data = pd.concat([pd.read_csv(os.path.join(folder_path, file_name)) for file_name in file_names])
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    original_data = pd.read_csv(file_path)
    print(f"Number of records in '{file_name}': {len(original_data)}")
print(f"Number of records in {extracted_string} merged file: {len(merged_data)}")
merged_data.to_csv(output_path, index=False)

