from navigating_data import *
from calling_data import call_all_data
from import_params import *

print("\nUse the save_in_pandas('dataset_id') function to import data")
print('\nSee the README file for the structure of the imported data')
print('\n-------------------------------------------------------')

## For testing

def return_data(dataset_id):
    return re_format_data(call_all_data(dataset_id))

## SAVES ALL DATA FROM DATASET ID TO DICTIONARY. FIRST SET OF KEYS BEING
## THE COUNTRY / JURISDICTION THE DATA APPLIES TO, THE SECOND SET OF KEYS
## BEING A SUMMARY OF THE DATA. SUMMARY INCLUDES INDICATOR TITLE & OTHER
## PARAMETERS SPECIFIC TO THAT DATASET.

import pandas as pd

def save_in_pandas(dataset_id):
    ## Pulls raw_data from API
    raw_data = call_all_data(dataset_id)

    ####################################
    #### Create reference variables ####
    ####################################

    ## A directory for OECD assigned values and corresponding attributes
    def_directory = create_directory(raw_data)
    ## A list of all of the keys for directory
    attributes = list(def_directory.keys())
    ## Re-Format Directory
    directory = {}
    for x in range(len(attributes)):
        directory.update(def_directory[attributes[x]])
    ## A list of all of the attributes for the dataset
    attributes = list(directory.keys())

    ##########################################
    ## Test compatibility and format output ##
    ##########################################

    try:
        ## Determine whether "Country" is one of the attributes
        #### FUTURE UPGRADE: Make list of all of the possible variables for
        #### country and save it to this file so that this function can loop
        #### through datasets that have a different name for this attribute
        keys = list(directory['Country'].values())
        ## Create variable for output
        output = {}
        ## Populate output with keys
        for x in range(len(keys)):
            output[keys[x]] = {}
    except KeyError:
        ## When looping through OECD data, use this to gather Dataset ID's that
        ## were not compatible with the function (those without 'Country' param)
        return dataset_id

    #################################################################
    ## Decide how attribute data is utilized (table name or index) ##
    #################################################################

    ## Options for each output variable
    attr_len = {}
    for x in range(len(attributes)):
        #### Exclude country from filter
        if attributes[x] != 'Country':
            attr_len[attributes[x]] = len(directory[attributes[x]])
    ## Find the size of the largest attribute
    attr_values = list(attr_len.values())
    index_size = max(attr_values)
    ## For attributes that warrant second tables for country/indicator pair
    relevant = []
    ## For attribute(s) with largest amount of values
    index_candidates = []
    for x in range(len(attributes)):
        #### Exclude country from filter
        if attributes[x] != 'Country':
            #### Populate relevant attributes
            if attr_len[attributes[x]] > 1:
                relevant.append(attributes[x])
            #### Populate index_candidates
            if attr_len[attributes[x]] == index_size:
                index_candidates.append(attributes[x])
    if len(index_candidates) > 1:
        ## Choose index from user input
        def manual_index_selection(index_attr, alt_index_attr):
            print('The largest variables are:\n')
            for x in range(len(index_candidates)):
                print(index_candidates[x])
            print('\nwhich would you like to be the index?')
            index = input()
            if index in attributes:
                return index
            else:
                print('your selection is not valid.\n')
                manual_index_selection(index_attr, alt_index_attr)
        index = manual_index_selection(index_attr, alt_index_attr)
    else:
        index = index_candidates[0]
    ## Remove index from list of other relevant variables
    relevant.remove(index)

    #################################
    ## Format / add data to output ##
    #################################

    ## A list of decoded OECD output
    data = re_format_data(raw_data)
    ## For table name creation
    indicator = params[dataset_id]['title']
    ## Loop through data and add observations to dataframe
    for x in range(len(data)):
        ## Single item in list
        datapoint = data[x]
        ## Data observations
        observations = datapoint['values']
        ## Time frame for observations
        time = list(observations.keys())
        ## Create title
        title = indicator
        ## Modify title if necessary
        if len(relevant) > 0:
            for y in range(len(relevant)):
                title += ', '
                title += datapoint[relevant[y]]
        ## Select the dataframe to add data to, if it doesn't exist, create it
        try:
            current_df = output[datapoint['Country']][title]
        except KeyError:
            output[datapoint['Country']][title] = pd.DataFrame()
            current_df = output[datapoint['Country']][title]
        for y in range(len(time)):
            current_df.at[datapoint[index], time[y]] = observations[time[y]]
    return output

### Saves all of the data available in a dataset to a SQLite database.
### Uses the country name as the database name, picks the attribute with
### the most possible selections to serve as the index, and creates the
### table title to include the dataset title and any other attributes
### necessary for said title.

#from database_access import save_from_pandas

#def save_to_sqlite(dataset_id):
#    data = save_in_pandas(dataset_id)
#    countries = list(data.keys())
#    for x in range(len(countries)):
#        titles = list(data[countries[x]].keys())
#        for y in range(len(titles)):
#            save_from_pandas(countries[x],
#                             titles[y],
#                             data[countries[x]][titles[y]])
