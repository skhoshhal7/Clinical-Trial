# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:38:02 2021

@author: nunna
"""
# hospitals.py

import pandas as pd

### HOSPITAL DATA 
def hospital():
    """
    This function creates a dataframe of hospitals and applies a 
    bed_scorer() function that gives each hospital a normalized score
    (the more beds the higher score)

    Returns
    -------
    Dataframe
        A datafram of hospitals with a score based of bed capacity.

    """
    hospitals = pd.read_csv('Hospitals.csv')
    
    selected_columns = hospitals[['ID', 'NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP',
                                  'TELEPHONE', 'COUNTY', 'TYPE', 'WEBSITE', 'COUNTYFIPS',
                                  'ST_FIPS', 'BEDS']]
    
    # select specific columns
    hospitals = selected_columns.copy()
    
    
    # remove Psychiatric hospitals
    hospitals.drop(hospitals[hospitals['TYPE'] == 'PSYCHIATRIC'].index, inplace = True)
    
    
    # make negative bed sizes set to mean
    mean_bed = round(hospitals['BEDS'].mean(), 0)
    temp = hospitals['BEDS'] <= 0
    hospitals.loc[temp, 'BEDS'] = mean_bed
    
    # fill NaN row
    hospitals.fillna({'ST_FIPS': 28, 'BEDS': mean_bed}, inplace=True)
    
    
    min_bed = hospitals['BEDS'].min()
    max_bed = hospitals['BEDS'].max()
    
    def bed_scorer(b):
        """
        This function is applied to the hospital 'BEDS' column and returns
        a normalized score based off the number of beds.

        Parameters
        ----------
        b : hospital 'BEDS' value
            An integer representing the number of beds each hospital has.

        Returns
        -------
        score : float
            A normalized score.

        """
        score = (b - min_bed) / (max_bed - min_bed)
        return score
    
    hospitals['Bed_Score'] = hospitals['BEDS'].apply(bed_scorer)
    
    # WEIGHT THE SCORES
    col=hospitals['Bed_Score'].apply(lambda x: 5 * x) 
    hospitals['Bed_Score'] = col 
    
    hospitals['Hospital_Score'] = 0

    return hospitals




