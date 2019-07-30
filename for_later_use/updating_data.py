''' The API has the capability to add datapoints that were either
added or updated after a certain point in time. These functions will
reference/create/update timestamp files in order to utilize this capability.
'''

import datetime

def last_timestamp(PARAMETERS, FOR, TITLE):
    ''' Returns the last timestamp as a string if it exists,
    None if it does not
    '''
    file_name = PARAMETERS + '_'  + FOR + '_' + TITLE + '.txt'
    try:
        with open('file.txt', 'r') as inf:
            last_timestamp = inf.read()
            inf.close()
        return last_timestamp
    except FileNotFoundError:
        return None

def update_timestamp(PARAMETERS, FOR, TITLE):
    ''' Saves the timestamp as a text file
    '''
    file_name = PARAMETERS + '_'  + FOR + '_' + TITLE + '.txt'
    now = datetime.datetime.now()
    now = now.strftime('%Y-%m-%d%%%H%M:%S')
    timestamp = open(file_name, 'w')
    timestamp.write(now)
    timestamp.close()










###########################
### Updated After Query ###
###########################

# Returns the observations inserted/updated since that point in time.

# Format:

# 2014-02-16
# 2014-02-16%2021:32
# 2014-02-16%2021:32:50
