import time
import requests
import sys
import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

databases_search_results = 'https://data.oecd.org/searchresults/?hf=20&b=0&r=f/type/datasets/api+access&l=en'

def load_entire_page(driver, SCROLL_PAUSE_TIME):
    ''' Scroll to the bottom of the page until all search results
    are loaded. Credit to Artjom B. on stackoverflow '''
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def pull_dataset_ids(link):
    ''' Returns all of the database IDs
    '''
    output = {}
    failed_databases = []
    ## Launch webdriver @ search results link
    driver = webdriver.Chrome()
    driver.get(link)
    ## Load all results by scrolling to the bottom of the page
    load_entire_page(driver, 1.5)
    ## Finds the elements that include the necessary links
    all_dbs = driver.find_elements_by_class_name("item")
    ## Loops through all_dbs in a new driver to gather necessary data
    driver_2 = webdriver.Chrome()
    for x in range(len(all_dbs)):
        try:
            ## For each dataset in the search results, extract link and title
    	    title = all_dbs[x].find_element_by_class_name("item-title").text
    	    link = all_dbs[x].get_attribute("data-identifier")
    	    ## Redirects to overview page for dataset
    	    driver_2.get(link)
    	    time.sleep(20)
    	    ## Gets to page necessary for extracting dataset id
    	    driver_2.find_element_by_class_name("action-data-2").click()
    	    time.sleep(15)
    	    driver_2.switch_to.window(driver_2.window_handles[1])
    	    time.sleep(1)
    	    ## Saves link as dataset_id and removes everything other than dataset_id
            ## if/else statement determines bad links and adds them to the list
    	    dataset_id = driver_2.current_url
    	    dataset_id_2 = dataset_id.replace('https://stats.oecd.org/viewhtml.aspx?datasetcode=', '')
            if dataset_id != dataset_id_2:
                dataset_id = dataset_id_2.replace('&lang=en', '')
        	    ## Saves necessary data to output
        	    output[dataset_id] = title
            else:
                failed_databases.append(title)
        except(TimeoutException, NoSuchElementException):
            failed_databases.append(title)
        ## Closes current window and switches to only window open
        if len(driver_2.window_handles) > 1:
            driver_2.close()
            driver_2.switch_to.window(driver_2.window_handles[0])
    ## Close drivers
    driver_2.close()
    driver.close()
    return [output, failed_databases]




results = pull_dataset_ids(databases_search_results)
sys.stdout = open('dataset_ids.txt', 'w')
print(results[0])
sys.stdout = open('failed_datasets.txt', 'w')
print(results[1])





#################################################################################
################### Potential improvement to timing pageloads ###################
#################################################################################

## https://stackoverflow.com/questions/28928068/scroll-down-to-bottom-of-infinite-page-with-phantomjs-in-python/28928684#28928684

#################################################################################
######################### Eliminating failed databases ##########################
#################################################################################

''' This code snippet would be utilized directly above the lines where
the drivers are closed in the pull_dataset_ids() function. Idea is to
have the function modify the output variable to include the datasets
that were left behind, and modify failed_databases to only include those
that failed again.
'''
### Works through failed databases
# while len(failed_databases) > 0:
#     reroute_by_title(driver, driver_2, failed_databases, output)

''' This function would need to also implement a feature where it can scrape
to see if a function was replaced, and if so, by what. It would also need to
find a way around dead links and be able to scan the substitutes. Reference
failed_datasets.txt from the original mining to understand the redirections
necessary to program into this function.
'''
#def reroute_by_title(driver, second_driver, titles, dictionary):
#    ''' Finds dataset IDs for previously failed datasets
#    '''
#    failed_dbs = []
#    for x in range(len(titles)):
#        try:
#            ## Gathers link on webpage by title
#            link = driver.find_element_by_partial_link_text(titles[x]).get_attribute('href')
#            ## Pulls link on second_driver
#            second_driver.get(link)
#            time.sleep(30)
#            ## Gets to page necessary for extracting dataset id
#            second_driver.find_element_by_class_name("action-data-2").click()
#            time.sleep(30)
#            second_driver.switch_to.window(driver_2.window_handles[1])
#            time.sleep(1)
#            ## Saves link as dataset_id and removes everything other than dataset_id
#            ## if/else statement determines bad links and adds them to the list
#            dataset_id = second_driver.current_url
#            dataset_id_2 = dataset_id.replace('https://stats.oecd.org/viewhtml.aspx?datasetcode=', '')
#            if dataset_id != dataset_id_2:
#                dataset_id = dataset_id_2.replace('&lang=en', '')
#                ## Saves necessary data to output
#                dictionary[dataset_id] = title
#            else:
#                ## Records failed database
#                failed_dbs.append(title)
#        except(TimeoutException, NoSuchElementException):
#            ## Records failed database
#            failed_dbs.append(title)

''' May or may not be worth continuing to build this out. Some links
are dead, but other links lead to other indicators that were not
in the search results. Some were replaced, in some of these instances,
the dataset that replaced it was picked up in the original mining. In
the first successful execution of this code, 7 datasets were failures,
and of those 7, only 1 was due to a timeout. I deemed it easier to
handle this part manually for now. See below for the original draft of
the code and instructions on implementation.
'''
