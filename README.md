# Navigating the OECD API in iPython

## How to use

## Current Capabilities:
  * Pull all of the data from a dataset
    * Load pull_data.py file
      * Dependencies: import_params.py, navigating_data.py, calling_data.py

    * Use dataset_ids file to locate the dataset you wish to load

  * Pull data in (raw-ish) dictionary format:
      * Raw-ish because the data is decoded, but not formatted in the most
        user-friendly way
      * Use the return_data() function
        * input: string, Dataset ID

  * Pull data in Pandas DataFrame format
    * Use the save_in_pandas() function
      * input: string, Dataset ID
      * output: dict, in the following format
        * {Country : {Indicator : {Additional Criteria (If applicable) : pd.DataFrame}}}
        * If no additional criteria applies, the value corresponding to the indicator is a pd.DataFrame as opposed to a dictionary

  * LIMITATIONS
    * OECD API may be omitting datapoints due to calls that are too large
    * Only works with Dataset IDs that have the 'Country' parameter, if a
      Dataset ID does not have this parameter, output will be the Dataset ID

## Capabilities to be added:

  * Calling less data in an API call
    * Progress on this front can be seen in the summary of the calling_data.py file below

  * Storing Data in MongoDB and SQLite format
    * Progress on this front can be seen in the summary of the database_access.py file below

  * Timestamping and updating databases based on last API call
    * Not much progress has been made on this front. The updating_data.py file is a start

## File path 

### src: Source Code

  src/import\_params.py
    * Imports the reference dictionaries of dataset\_params and dataset\_ids
      from the .json files in the data folder. See below for their structures

  src/navigating\_data.py
    * Raw OECD output uses integers to describe the parameters of data in question
      this file gives the tools necessary to assign readability to the parameters

      * Creates references for the files in question
        * create\_directory()
          * Decodes parameters
        * time\_reference()
          * Decodes time periods in OECD

      * Translates and re-formats the data from raw OECD output
        * re\_format\_data()
          * Input: raw OECD output
          * Output: decoded OECD output
        * translate\_key() assigns attributes based on reference files
          * utilized within re\_format\_data()

  src/calling_data.py
    * The only function necessary at the moment is call_all_data()
      * Input: Dataset ID, Output: Raw OECD data
    * Other functions and deprecated code will allow capabilities for more
      specific API calls. Deprecated code needs to be updated to reflect the
      change from object oriented programming to native data structures

  src/pull_data.py
    * Contains the two functions shown in the Current Capabilities section above

### data: Self Explanatory

  data/archives
    * Includes scraper programs and the files used to create the files necessary for
      the program to run.

  data/dataset_params.json
    * Includes all reference data for each dataset
    * Follows the following format:
        > {DATASET_ID : {'title' : TITLE,
        >               'params' : {PARAMETER : {'codelist_id' : CODELIST ID,
        >                                        'required' : BOOLEAN,
        >                                        'count' : COUNT,
        >                                        'values' : {DESCRIPTION : VALUE,
        >                                                    DESCRIPTION : VALUE}}}}}

  data/dataset_ids.json
    * Abbreviated version of dataset_params.json
    * {DATASET_ID : TITLE}

### for_later_use:
  * Files for future capabilities. Will be summarized later on

## To Do: 

1.  Finish storing data in json format
2.  Create global variables
3.  Link to SQLite and MongoDB
4.  Finish the updating_data file
6.  LABEL, LABEL, LABEL
