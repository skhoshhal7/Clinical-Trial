# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 15:08:08 2021

@author: nunna
"""

# main script

import pandas as pd
import census as cen
import census_score as cs
import cdc as c
import hospitals as h
import hospital_score as hs
import clinical_trial_search as cts
from datetime import datetime

def main():
    """
    Libraries: pandas
    Function imports: census, census_score, cdc, hospitals, hospital_score, clinical_trial_search
    
    This Program starts by importing the census and hospital dataframes via their functions.
    
    Then it prompts users to input:
        1) cancer condition
        2) age group
        3) racial/ethnic group
        4) sex/gender
    
    Following:
        - Uploads and scores the CDC dataframe based on the selected 
        condition, racial group, and sex/gender
        - Scores census data based on condition rates, age, racial group population
        - Scores hospital data based on condition, age
        - Merges the scored CDC, Census, and Hospital dataframes
        - Totals score and sorts by highest score
        - Accesses the clinical trials function to select and rank the top n scored
        hospitals by # of clinical trials for the specified condition
        - Exports an excel file with the top n hospitals and website information.
    

    

    Returns
    -------
    The Program loops until the user quits.
    
    Exports an excel file.
    
    Note: should save the excel file  as something different (or copy paste results)
    if planning to rerun the program immediately for different results,
    as it will be written over.

    """
    pd.set_option('display.expand_frame_repr', False)
    
    # import census and hospital dataframes
    census = cen.census()
    hospitals = h.hospital()
    
    # program loop
    enter = -1
    while enter != 0:
        try:    
            print('----------------------------------------------------------------')
            print('                      \n***MAIN MENU***\n')
            print('----------------------------------------------------------------\n\n')  
            enter = int(input("Enter '1' to enter or '0' to quit: "))
            if enter == 0:
                break
            elif enter != 1:
                print('\n\n\n\n\n----------------------------------------------------------------')
                print('\n!!! INVALID ENTRY !!!\n')
                print('----------------------------------------------------------------\n\n\n\n\n')
                continue
        except:
            print('\n\n\n\n\n----------------------------------------------------------------')
            print('\n!!! INVALID ENTRY !!!\n')
            print('----------------------------------------------------------------\n\n\n\n\n')
            continue
        condition = -1
        while condition != 0:    
            try:
                print('\n----------------------------------------------------------------')
                print('\nChoose from the following cancer types:\n')
                print('1)  Female Breast Cancer')
                print('2)  Corpus and Uterus, NOS')
                print('3)  Ovary')
                print('4)  Prostate')
                print('5)  Lung and Bronchus Cancer')
                print('6)  Colon and Rectum')
                print('7)  Non-Hodgkin Lymphoma')
                print('8)  Leukemias')
                print('9)  Pancreas')
                print('10) Liver\n')
                condition = int(input("Enter the # next to your selection or '0' to exit to main menu: "))
                if condition == 0:
                    break
                elif condition in range(1,11):
                    break
                else:
                    print('\n\n\n\n\n----------------------------------------------------------------')
                    print('\n!!! INVALID ENTRY !!!')
                    continue
            except:
                print('\n\n\n\n\n----------------------------------------------------------------')
                print('\n!!! INVALID ENTRY !!!')
                condition = -1
        if condition == 0:        
            print('\n----------------------------------------------------------------\n\n\n\n\n')
            continue
        age = -1
        while age != 0:
            try:
                print('\n----------------------------------------------------------------')
                print('\nChoose from the following age ranges:\n')
                print('1) Under 18 years')
                print('2) 18 to 64 years')
                print('3) 65+ years')
                print('4) All ages\n')
                age = int(input("Enter the # next to your selection or '0' to exit to main menu: "))
                if age == 0:
                    break
                elif age in range(1,5):
                    break
                else:
                    print('\n\n\n\n\n----------------------------------------------------------------')
                    print('\n!!! INVALID ENTRY !!!')
                    continue
            except:
                print('\n\n\n\n\n----------------------------------------------------------------')
                print('\n!!! INVALID ENTRY !!!')
                age = -1
        if age == 0:
            print('\n----------------------------------------------------------------\n\n\n\n\n')
            continue
        race = -1
        while race != 0:
            try:
                print('\n----------------------------------------------------------------')
                print('\nChoose from the following racial/ethnic groups:\n')
                print('1) All Races and Ethnicities')
                print('2) White')
                print('3) Black')
                print('4) American Indian and Alaskan Native')
                print('5) Asian and Pacific Islander')
                print('6) Hispanic/Latino\n')
                race = int(input("Enter the # next to your selection or '0' to exit to main menu: "))
                if race == 0:
                    break
                elif race in range(1,7):
                    break
                else:
                    print('\n\n\n\n\n----------------------------------------------------------------')
                    print('\n!!! INVALID ENTRY !!!')
                    continue
            except:
                print('\n\n\n\n\n----------------------------------------------------------------')
                print('\n!!! INVALID ENTRY !!!')
                race = -1
        if race == 0:
            print('\n----------------------------------------------------------------\n\n\n\n\n')
            continue
        gender = -1
        while gender != 0:
            try:
                print('\n----------------------------------------------------------------')
                print('\nChoose from the following gender/sex groups:\n')
                print('1) Male and Female')
                print('2) Male Only')
                print('3) Female Only\n')
                gender = int(input("Enter the # next to your selection or '0' to exit to main menu: "))
                if condition in range(1,4) and gender in range(1,3):
                    print('\n\n\n\n\n----------------------------------------------------------------')
                    print('\nERROR: Selection of cancer type and gender/sex are invalid.')
                    print('Reselect gender/sex.')
                    continue
                if condition == 4 and gender in [1,3]:
                    print('\n\n\n\n\n----------------------------------------------------------------')
                    print('\nERROR: Selection of cancer type and gender/sex are invalid.')
                    print('Reselect gender/sex.')
                    continue
                if gender == 0:
                    break
                elif gender in range(1,4):
                    break
                else:
                    print('\n\n\n\n\n----------------------------------------------------------------')
                    print('\n!!! INVALID ENTRY !!!')
                    continue
            except:
                print('\n\n\n\n\n----------------------------------------------------------------')
                print('\n!!! INVALID ENTRY !!!')
                gender = -1
        if gender == 0:
            print('\n----------------------------------------------------------------\n\n\n\n\n')
            continue
        print('\n\n\n\n\n----------------------------------------------------------------')
        
        # Upload CDC dataframe and score the states
        cdc = c.findstate(condition, gender, race)
        
        
        # score the counties based on age, race, cancer rate
        census_df = cs.census_score(census, age, race, condition)
        
        
        # score the hospitals based on cancer and age
        hospitals_df = hs.hospital_scorer(hospitals, condition, age)
        
        print()
        
        # merge the tables together
        merge1 = pd.merge(census_df, cdc)
        merge2 = pd.merge(hospitals_df, merge1)
        merge2['Score_Total'] = merge2[['Bed_Score','Hospital_Score','Census_Score','CDC_Score']].sum(axis=1)
        
        # sort the table by highest total score
        merge2.sort_values(by='Score_Total', ascending = False, inplace=True)
        
        
        col_names = ['Breast Cancer',
                 'Uterus cancer',
                 'Ovary cancer',
                 'Prostate cancer',
                 'Lung cancer',
                 'Colon cancer',
                 'Non-Hodgkin Lymphoma',
                 'Leukemia',
                 'Pancreas cancer',
                 'Liver cancer']
        cond = col_names[condition - 1]
        
        # edit [0:00] to select amount of hospitals
        # Calls clinical trial function to rank based on trial history
        cts_df = cts.hospital_rank(merge2[0:20], cond)
        
        # Creating result DataFrame
        final_df = pd.merge(
            cts_df,
            merge2,
            how='inner',
            left_on='hospital',
            right_on='NAME'
        ).sort_values('study_count', ascending=False).reset_index()[[
            'hospital','hospital_website','CITY','STATE','hospital_telephone',
            'study_count','BEDS','Census_Score','CDC_Score','Score_Total'
        ]]
        
        # Display top 10 ranking with contact telephone
        print(final_df[[
            'hospital','CITY', 'STATE','hospital_telephone',
        ]].head(10))
        
        
        print("\nIn your folder, you can retrieve your full list in the excel file: 'ranked_hospital_partner_prospects...'.xlsx\n")
        
        # exports final DataFrame as excel sheet
        final_df.to_excel(
            'ranked_hospital_partner_prospects_'+ \
                datetime.now().strftime('%Y%m%d_%H.%M.%S') +'.xlsx',
            index=False
        )
        
if __name__ == '__main__':
     main()











