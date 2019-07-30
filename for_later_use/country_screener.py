'''

This script includes the function sort_by_country() which
takes one argument, the name of a country (as a string).

The output of this function is a dictionary with the keys
'yes' and 'no'. The values that correspond with these keys are
lists of Dataset ID's that either do include that country in
its data (yes) or dont (no).

Prior to defining the function, this script will create a list
of all of the datasets that incorporate country as a parameter
for use within the function.

'''

## Import data/dataset_params.json
from import_params import *

###############################
## Create Variables ###########
###############################

#### VALID = LIST OF DATASET IDS WITH LOCATION, COUNTRY, OR COU PARAM
valid = []

#### NOT VALID = LIST OF DATASET IDS THAT DO NOT INCLUDE THESE PARAMS
not_valid = []

for x in range(len(dataset_ids)):
    ## LIST OF PARAMS FOR DATASET ID
    param_list = list(params[dataset_ids[x]]['params'].keys())
    ## SORT THROUGH DATASETS W/ POTENTIAL PARAM NAMES FOR COUNTRY
    if "LOCATION" in param_list:
        valid.append(dataset_ids[x])
    elif "COU" in param_list:
        valid.append(dataset_ids[x])
    elif "COUNTRY" in param_list:
        valid.append(dataset_ids[x])
    ## LIST THOSE THAT DO NOT INCLUDE SUCH PARAMETER
    else:
        not_valid.append(dataset_ids[x])

#### FUNCTION TAKES A COUNTRY ARGUMENT AND SORTS
#### THROUGH POSSIBLE VALUES FOR EACH PARAM

def sort_by_country(country):
    output = {'yes' : [],
              'no' : []}
    for x in range(len(valid)):
        try:
            values_list = list(params[valid[x]]['params']['COU']['values'].keys())
        except KeyError:
            try:
                values_list = list(params[valid[x]]['params']['COUNTRY']['values'].keys())
            except KeyError:
                values_list = list(params[valid[x]]['params']['LOCATION']['values'].keys())
        if country in values_list:
            output['yes'].append(valid[x])
        else:
            output['no'].append(valid[x])
    return output
