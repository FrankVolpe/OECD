##########################################################################
## THIS FUNCTION SHOWS WHAT THE NUMBER NEXT TO A DATAPOINT IN THE OECD  ##
## API OUTPUT IS TRANSLATED TO IN TERMS OF THAT DATAPOINT'S TIME PERIOD ##
##########################################################################

def time_reference(raw_data):
    values = raw_data['structure']['dimensions']['observation'][0]['values']
    time_period = {}
    for x in range(len(values)):
        try:
            time_period[x] = values[x]['id']
        except KeyError:
            continue
    return time_period

########################################################################
## THIS IS USED FOR NAVIGATING THE KEYS OF THE OECD API OUTPUT #########
## EXAMPLE OF A KEY FOR A DATAPOINT IN OECD OUTPUT: '1:3:0:2' ##########
## EACH NUMBER REFLECTS AN ATTRIBUTE TO THIS DATAPOINT #################
## THE ORDER OF THESE NUMBERS IS REFLECTED BY KEYPOSITION ##############
########################################################################
## WHAT THE KEYPOSITION IS AS WELL AS WHAT THE NUMBER ACTUALLY #########
## MEANS IS SHOWN IN THE DIRECTORY. USE THIS TO NAVIGATE / MANIPULATE ##
## THE DATA. ###########################################################
########################################################################

def create_directory(raw_data):
    directory = {}
    series = raw_data['structure']['dimensions']['series']
    for x in range(len(series)):
        directory[series[x]['keyPosition']] = {}
        directory[series[x]['keyPosition']][series[x]['name']] = {}
        values = series[x]['values']
        for y in range(len(values)):
            directory[series[x]['keyPosition']][series[x]['name']][y] = values[y]['name']
    return directory

##################################################################
## input key and directory, return dict of that keys attributes ##
##################################################################

def translate_key(key, directory):
    splitted = key.split(':')
    translation = {}
    for x in range(len(splitted)):
        parameter_in_question = list(directory[x].keys())[0]
        selection = int(splitted[x])
        param_value = directory[x][parameter_in_question][selection]
        translation[parameter_in_question] = param_value
    return translation

def re_format_data(raw_data):
    output = []
    ## Raw data excluding documentation
    data = raw_data['dataSets'][0]['series']
    ## A directory for OECD assigned values and corresponding years
    time_period = time_reference(raw_data)
    ## A directory for OECD assigned values and corresponding attributes
    directory = create_directory(raw_data)
    ## Keys of all values in the raw data
    all_keys = list(data.keys())
    ## Loop through all keys
    for x in range(len(all_keys)):
        ## Temporary variable for storing data from individual datapoint
        observations = {}
        ## Year and value of each datapoint
        datapoint = data[all_keys[x]]['observations']
        ## All other attributes surrounding that datapoint
        attributes = translate_key(all_keys[x], directory)
        ## Years that datapoint are available (not decoded)
        years = list(datapoint.keys())
        ## Decodes year and saves as a key in a dictionary, values = data
        for y in range(len(years)):
            ## Decode Year
            year = time_period[int(years[y])]
            ## Save in dict
            observations[year] = datapoint[years[y]][0]
        ## Add observations to datapoint
        attributes['values'] = observations
        output.append(attributes)
    return output
