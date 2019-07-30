import requests
import json
import pandas as pd


def call_all_data(dataset_id):
    ''' returns all data for dataset in question
    '''
    return requests.get("http://stats.oecd.org/sdmx-json/data/" + dataset_id).json()

def call_link(link, parameters=None):
    if len(link) <= 1000:
        return requests.get(link, params=parameters).json()
    else:
        print("API HTML is too long.")

### params variable should be equal to the 'params' file created by import_params.py

def is_required(params, dataset_id):
    ''' Prints all possible parameters and whether or not they are required
    '''
    df = pd.DataFrame(columns=['Required'])
    param_list = list(params[dataset_id]['params'].keys())
    for x in range(len(param_list)):
        df.at[param_list[x], 'Required'] = params[dataset_id]['params'][param_list[x]]['required']
    print(df)

### params variable should be equal to the 'params' file created by import_params.py
### param variable should be one of the params available for that dataset

def display_values(params, dataset_id, param):
    try:
        values_dict = params[dataset_id]['params'][param]['values']
        print(pd.DataFrame.from_dict(values_dict, orient='index', columns=['Description']))
    except KeyError:
        print('The key you entered is not valid')


############################################
## Below listed code is deprecated due to ##
## switch away from using objects ##########
############################################


#def build_html(self, mandatory_URL_data, agency_name = 'all'):
#   ''' builds link with output from create_html()
#
#   ASSUMPTIONS THAT MAY LEAD TO FUTURE ERRORS:
#   1. All datasets have requested the parameters be added in the order they
#   are presented in that datasets 'documentation'
#   2. Assumes the user enters these correctly and does not enter the same choice
#   twice (or doesn't skip an entry)
#   '''
#   link = "http://stats.oecd.org/sdmx-json/data/" + self.dataset_id + '/'
#   # Create list of params to be added
#   params = list(mandatory_URL_data.keys())
#   # Format params to be added to the link correctly
#   params_2 = {}
#   for x in range(len(params)):
#       if self.params[params[x]].count != 0:
#           params_2[self.params[params[x]].count] = '.' + mandatory_URL_data[params[x]]
#       else:
#           params_2[self.params[params[x]].count] = mandatory_URL_data[params[x]]
#   for x in range(len(params)):
#       link += params_2[x]
#   link += '/' + agency_name
#   return link
#
#def create_html(self):
#   ''' Walks user through API URL construction
#   '''
#   ## Select the parameters you wish to include, automatically includes
#   ## required parameters
#   print('Select the optional parameters you would like to include.')
#   print('Optional parameters are as follows: \n')
#   params = list(self.params.keys())       ## all parameters
#   params_for_URL = []                     ## parameters to be included
#   mandatory_URL_data = {}                        ## {parameter : selection}
#   for x in range(len(params)):
#       if self.params[params[x]].required == True:
#           params_for_URL.append(params[x])
#
#   ######################################################################### Making URL builder support only
#   #    if self.params[params[x]].required == False:                       # mandatory inputs at this moment,
#   #        print('would you like to include ', params[x], '?\n y/n')      # these lines of code will change
#   #        user_input = input()                                           # that to allow optional parameters.
#   #        if user_input == 'y':                                          #
#   #            params_for_URL.append(params[x])                           # Need to separate the two so build_html()
#   #    else:                                                              # can determine whether or not it is mandatory
#   #        params_for_URL.append(params[x])                               #
#   #########################################################################
#
#   ## Selecting which option to use for each parameter selected
#   for x in range(len(params_for_URL)):
#       self.display_values(params_for_URL[x])
#       parameter_choice = input('Which would you like to include?\nEnter "all" to include all params')
#       ## Creates API call in proper format for all requests
#       if parameter_choice == 'all':
#           values = list(self.params[params[x]].values.keys())
#           for y in range(len(values)):
#               if y != 0:
#                   parameter_choice += '+'
#                   parameter_choice += values[y]
#               else:
#                   parameter_choice = values[y]
#       ## for selection of certain criteria
#       else:
#           additional_input = input('Enter more desired selections, or "n" to stop\n')
#           while additional_input != 'n':
#               parameter_choice += '+'
#               parameter_choice += additional_input
#               additional_input = input('Enter "n" to stop\n')
#       mandatory_URL_data[params_for_URL[x]] = parameter_choice
#   return build_html(mandatory_URL_data)
