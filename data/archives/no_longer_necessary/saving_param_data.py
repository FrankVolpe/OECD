from bs4 import BeautifulSoup
import requests
import json
import time
import sys

from import_ids import import_ids

all_dataset_ids = list(import_ids().keys())

def pull_params(dataset_id):
    ''' SUMMARIZE
    '''
    ## Create empty list to store params
    params = []
    ## Pull Data From API's individual dataset documentation
    base_link = "http://stats.oecd.org/restsdmx/sdmx.ashx/GetDataStructure/"
    api_html = base_link + dataset_id
    data = BeautifulSoup(requests.get(api_html).content,"lxml-xml")
    ## Break down data to pull necessary information
    concepts = data.Concepts.contents
    ## Loop through data to mine params
    for x in range(len(concepts)):
        concept_id = concepts[x].attrs['id']
        if concept_id != 'OBS_VALUE':
            params.append(concept_id)
    return {dataset_id : params}

output = {}
failures = []

for x in range(len(all_dataset_ids)):
    try:
        output.update(pull_params(all_dataset_ids[x]))
    except:
        failures.append(all_dataset_ids[x])
    time.sleep(5)

with open('dataset_params.json', 'w') as outfile:
    json.dump(output, outfile)

sys.stdout = open('failed_datasets.txt', 'w')
print(failures)
