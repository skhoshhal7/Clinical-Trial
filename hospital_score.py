# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:11:33 2021

@author: nunna
"""

def hospital_scorer(df, condition, age):
    """
    This function provides an additional score to hospitals based off
    the age and condition chosen.
    
    If the cancer chosen is one of the first three, hospitals of type
    'WOMEN' receive an additional score of 100.
    
    If the cancer chosen is 'Prostate', hospitals of type
    'WOMEN' receive a score of -100.
    
    If the age group '<18 years' is chosen, hospitals of type
    'CHILDREN' receive an additional score of 100.

    Parameters
    ----------
    df : dataframe
        Hospital dataframe.
    condition : int
        An integer representing a cancer type selected by the user.
    age : int
        An integer representing an age group selected by the user.

    Returns
    -------
    df : dataframe
        The hospital dataframe returned with an additional score column.

    """
    for i in range(len(df)):
        if condition in range(1,4):
            df.loc[(df['TYPE'] == 'WOMEN'),'Hospital_Score'] = 100
        elif condition == 4:
            df.loc[(df['TYPE'] == 'WOMEN'),'Hospital_Score'] = -100
        elif age == 1:
            df.loc[(df['TYPE'] == 'CHILDREN'),'Hospital_Score'] = 100
    return df



    






