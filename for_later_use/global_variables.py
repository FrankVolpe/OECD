''' For setting parameters on URL builds
'''

###################
###################
## Query options ##
###################
###################

start = 'startPeriod'
end = 'endPeriod'
dimnsion = 'dimensionAtObservation'
detail = 'detail'
update = 'UpdatedAter'

######################################
### Dimension At Observation Query ###
######################################

# Dimension to be attached at the observation level, or “AllDimensions”. If this parameter is not set, then the default value order is:
# Output of AllDimensions = dict with 5 indexes (0:0:0:0:0)
# In order: Location, Subject, Measure, Frequency, Time

observation_dimension = {
    'time' : "TimeDimension",              # ************
    'measure' : "MeasureDimension",        # ************
    'all' : "AllDimensions"               # Flat list of observations without any grouping.
    }

####################
### Detail Query ###
####################

# Specifies the desired amount of information to be returned
# DEFAULT = Full - all data and documentation, including annotations

detail_query = {
    'data' : "DataOnly",            # Attributes – and therefore groups – will be excluded
    'keys' : "SeriesKeysOnly",      # Returns series elements dimensions that make up the series keys
    'none' : "NoData"               # Returns the groups and series, including attributes and annotations, without observations
    }

#####################################
### Start Period/End Period Query ###
#####################################

# Possible Formats:
# year
# year-semester: <year>-S1 – <year>-S2
# year-quarter: <year>-Q1 –  <year>-Q4
# year-month: <year>-M1 –  <year>-M12
