import json
import sys

sys.path.insert(0, 'OECD/')

with open('data/dataset_params.json', 'r') as file:
    txt = file.read()
    params = json.loads(txt)
    file.close()

with open('data/dataset_ids.json', 'r') as file:
    txt = file.read()
    dataset_ids = json.loads(txt)
    file.close()

print('------------------------------------------------------')
print('\nDataset IDs and corresponding parameters are stored in the "params" file')
print('\n"dataset_ids" is a reference for Dataset IDs and what datasets they pertain to')
print('\n------------------------------------------------------')
