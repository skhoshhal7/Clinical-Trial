# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:30:55 2021

@author: Jack Jacobs

LIBRARIES REQUIRED:
    pandas
    json
    selenium
    
FILES REQUIRED:
    Chrome driver for user's version of Google Chrome
        obtained from 'https://chromedriver.chromium.org/downloads'
    Kaggle hospitals CSV dataset
    

PROGRAMS REQUIRED:
    Google Chrome
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import json

def expr_string(condition, hospital):
    '''
    Generates a search ("expr") string for use in the clinicaltrials.gov
        API demo page, based on the desired condition and hospital
    'https://clinicaltrials.gov/api/gui/demo/simple_study_fields'

    Parameters
    ----------
    condition : string
        Medical condition to search.
    hospital : string
        Hospital (at which search result clinical trials are based)
            to search for.

    Returns
    -------
    expr_string : string
        A formatted search string for input into the "expr" field of the
            clinicaltrials.gov API demo page.
    '''
    
    expr_string = \
        f'{condition} AND ' + \
            'SEARCH[Location](AREA[LocationCountry]United States AND ' + \
            f'AREA[LocationFacility]{hospital})'
    
    return expr_string

def obtain_study_count(clinical_trial_search_results):
    '''
    Obtains the number of search results found from a clinicaltrials.gov
        JSON API search result string

    Parameters
    ----------
    clinical_trial_search_results : string
        Raw returned JSON-format search results.

    Returns
    -------
    study_count : int
        The number of search results found.
    '''
    
    results_dict = json.loads(clinical_trial_search_results)
    study_count = results_dict['StudyFieldsResponse']['NStudiesFound']
    
    return study_count

def hospital_rank(hospital_df, condition):
    '''
    Generates a normalized clinical trial experience score for each hospital
        in a list of hospitals based on the number of clinical trial
        search results returned for a given condition in the
        clinicaltrials.gov API, using that API's demo page
    'https://clinicaltrials.gov/api/gui/demo/simple_study_fields'

    Parameters
    ----------
    hospital_df : pandas.DataFrame
        A DataFrame of hospitals with columns 'NAME' and 'WEBSITE'.
    condition : string
        The medical condition of interest.

    Returns
    -------
    hospital_rank_df : pandas.DataFrame
        A DataFrame with columns 'hospital', 'hospital_website',
        'study_count', and 'normalized_study_count' sorted in descending
        order by 'study_count'.
    '''
    
    # Set up Chrome webdriver for Chrome 94
    path = 'chromedriver.exe'
    driver = webdriver.Chrome(path)
    
    # Opening search webpage
    clinicaltrials_search_url = \
        'https://clinicaltrials.gov/api/gui/demo/simple_study_fields'
    
    # Instantiating list to receive study count
    result_list = []
    
    # Instantiating counter in case of connection failure
    i = 0
    
    for hospital in hospital_df.NAME:
        # Iterating search process over the pd.Series of hospital names
        
        # Re-open search page
        driver.get(clinicaltrials_search_url)
        
        # Edit search terms
        expr_length = len(driver.find_element_by_name('expr').text)
        expr = driver.find_element_by_name('expr')
        expr.send_keys(Keys.BACK_SPACE * expr_length)
        expr.send_keys(expr_string(condition, hospital))
        
        # Edit search fields to return
        fields = driver.find_element_by_id('fields')
        fields.send_keys(Keys.BACK_SPACE * len(fields.text))
        fields.send_keys(
            'NCTId,BriefTitle,Condition,LocationFacility,OverallStatus'
        )
        
        # Edit search result range
        min_rnk = driver.find_element_by_id('min_rnk')
        min_rnk.send_keys(Keys.BACK_SPACE * 10)
        min_rnk.send_keys('1')
        
        max_rnk = driver.find_element_by_id('max_rnk')
        max_rnk.send_keys(Keys.BACK_SPACE * 10)
        max_rnk.send_keys('2')
        
        # Choosing JSON format
        fmt = driver.find_element_by_name('fmt')
        Select(fmt).select_by_value('json')
        
        # Sending search
        send = driver.find_element_by_id('SendRequestButton')
        send.click()
        
        # Allow search results to load
        # https://stackoverflow.com/questions/38363643/
        ## python-selenium-get-inside-a-document/38363681
        results_iframe = driver.find_element_by_id('ResponseFrame')
        driver.switch_to.frame(results_iframe)
        
        try:
            
            # Wait 10 seconds before throwing a connection error
            pre = WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'pre'))
            )
            
            # Set new result_list item to the number of matchingstudies found
            result_list.append(obtain_study_count(pre.text))
            
            i += 1
            
        except:
            print(
                f'Connection to ClinicalTrials.gov failed after {i} tries'
            )
            driver.quit()
        
        # Return Selenium webdriver to the webpage's main HTML frame
        driver.switch_to.default_content()
    
    # Close Chrome
    driver.quit()
    
    # Define new DataFrame by the results of the search
    hospital_rank_df = pd.DataFrame({
        'hospital':hospital_df.NAME,
        'hospital_website':hospital_df.WEBSITE,
        'hospital_telephone':hospital_df.TELEPHONE,
        'study_count':result_list
    }).sort_values('study_count', ascending=False)
    
    # Add field for normalized experience score based 'study_count'
    hospital_rank_df.loc[:,'normalized_study_count'] = \
        (hospital_rank_df.study_count - \
             hospital_rank_df.study_count.min()) / \
        (hospital_rank_df.study_count.max() - \
             hospital_rank_df.study_count.min())
    
    return hospital_rank_df




def main():
    # Each search takes 4.24 seconds on CMU wifi
    hospital_df = pd.read_csv('Hospitals.csv')[[
        'NAME','WEBSITE'
    ]]
    
    result_df = hospital_rank(hospital_df.iloc[0:20], 'lung cancer')
    result_df.to_excel('test_df.xlsx', index=False)
    
    print(result_df.head())
    
if __name__ == '__main__':
    main()
