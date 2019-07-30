'''
Creates a .json file with all of the information stored in previously
used OECD_dataset objects.

FORMAT:

{DATASET_ID : {'title' : TITLE,
               'params' : {PARAMETER : {'codelist_id' : CODELIST ID,
                                        'required' : BOOLEAN,
                                        'count' : COUNT,
                                        'values' : {DESCRIPTION : VALUE,
                                                    DESCRIPTION : VALUE}}}}}
'''

##  For some reason all of the values are being saved to each parameter.
##  Figure out why this is AND FUCKING FIX IT.

## IMPORT PACKAGES
from bs4 import BeautifulSoup
import requests
import json
import time
import sys

#############################################
## IMPORT DICT OF ALL DATASET IDS & TITLES ##
#############################################

def import_ids():
    with open('data/dataset_ids/dataset_ids.json', 'r') as file:
        dataset_ids = eval(file.read())
        file.close()
    return dataset_ids

## DICT - {ID : TITLES}
ids_and_titles = import_ids()

## LIST - ALL DATASET IDS
all_ids = list(ids_and_titles.keys())
#all_ids_test = ['HH_DASH', 'SNA_TABLE9_SNA93', "SNA_TABLE720R", "WEALTH"]

## To save as value whenever a PARAMATER key is created
## Later updated to include the correct values
default = {'codelist_id' : '',
           'count' : None,
           'required' : True,
           'values' : None,
           }

##########################################################
## Uses BeautifulSoup to pull information on Dataset ID ##
##########################################################

def pull_from_soup(dataset_id):
    ''' SUMMARIZE
    '''
    ## EMPTY DICT TO STORE PARAMS
    params = {}
    ## Pull Data From API's individual dataset documentation
    base_link = "http://stats.oecd.org/restsdmx/sdmx.ashx/GetDataStructure/"
    api_html = base_link + dataset_id
    data = BeautifulSoup(requests.get(api_html).content,"lxml-xml")
    ## Break down data to pull necessary information
    concepts = data.Concepts.contents
    codelist_ids = data.KeyFamilies.Components.contents
    values = data.CodeLists.contents
    ## Loop through data to mine params
    for x in range(len(concepts)):
        concept_id = concepts[x].attrs['id']
        if concept_id != 'OBS_VALUE':
            ## Save params
            params[concept_id] = default.copy()
            ## Find corresponding codelist_id
            if concept_id == codelist_ids[x].attrs['conceptRef']:
                add_codelist(params[concept_id], codelist_ids[x])
            ## Since this API is less than perfect, the next lines of code account
            ## for the possibility of discrepencies in the order of the parameters
            else:
                for y in range(len(codelist_ids)):
                    if concept_id == codelist_ids[y].attrs['conceptRef']:
                        add_codelist(params[concept_id], codelist_ids[y])
            if params[concept_id]['required'] == True:
                params[concept_id]['count'] = x
            ## Populates values with possible values in an API call
            try:
                ## Second exception for when values is shorter than concepts
                try:
                    if params[concept_id]['codelist_id'] == values[x].attrs['id']:
                        add_values(params[concept_id], values[x])
                    ## Since this API is less than perfect, the next lines of code account
                    ## for the possibility of discrepencies in the order of the parameters
                    else:
                        for y in range(len(values)):
                            if params[concept_id]['codelist_id'] == values[y].attrs['id'].strip():
                                add_values(params[concept_id], values[y])
                except IndexError:
                    if params[concept_id]['codelist_id'] == values[x-1].attrs['id']:
                        add_values(params[concept_id], values[x-1])
                    else:
                        ## Since this API is less than perfect, the next lines of code account
                        ## for the possibility of discrepencies in the order of the parameters
                        for y in range(len(values)):
                            if params[concept_id]['codelist_id'] == values[y].attrs['id'].strip():
                                add_values(params[concept_id], values[y])
            except AttributeError:
                continue
    return params

####################################################################
## MODIFIES DEFAULT TO INCLUDE CODELIST ID AND 'REQUIRED' BOOLEAN ##
####################################################################

def add_codelist(param_attrs, raw_codelist):
    try:
        param_attrs['codelist_id'] = raw_codelist.attrs['codelist']
        if raw_codelist.attrs['conceptRef'] == 'TIME':
            param_attrs['required'] = False
        elif raw_codelist.attrs['assignmentStatus'] == 'Conditional':
            param_attrs['required'] = False
        else:
            param_attrs['required'] = True
    except KeyError:
        param_attrs['required'] = True

###################################
## POPULATES DEFAULT WITH VALUES ##
###################################

def add_values(param_attrs, raw_values):
    param_attrs['values'] = {}
    for x in range(len(raw_values.contents)):
        values_at_x = raw_values.contents[x]
        try:
            value = values_at_x.attrs['value']
            description = values_at_x.Description
            param_attrs['values'][description.get_text()] = value
        except KeyError:
            continue

##########################
## Create and save file ##
##########################

output = {}
failures = []



for x in range(len(all_ids)):
    try:
        output[all_ids[x]] = {'params' : pull_from_soup((all_ids[x]))}
        output[all_ids[x]]['title'] = ids_and_titles[all_ids[x]]
    except:
        failures.append(all_ids[x])
    time.sleep(5)

with open('dataset_params.json', 'w') as outfile:
    json.dump(output, outfile)

sys.stdout = open('failed_datasets.txt', 'w')
print(failures)
