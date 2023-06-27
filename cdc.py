#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 11:37:42 2021

@author: huangtiffany
"""

def findstate(indication, gender, race):
    '''
    
    Generating a disease prevalence score for each state basesd on age-adjusted rate of cancer death (death per 100,000 people), 
    and cancer death count (data sorce: https://gis.cdc.gov/Cancer/USCS/#/AtAGlance/).
    The death rate and case count will be normalized by minus its minima value of all states then divided by the difference 
    between maxima and minima value. The weight of cancer dealth rate and case count are considered equal (wieght  = 0.5). 
    The formula for the scoring (CDC_Score):
    
    Case Count = cancer death count
    age-adjusted rate of cancer death = rate
    CDC_Score = (0.5 * ((case count - case count minima value) \ (case count maxima value - case count minima value)))
              + (0.5 * ((rate - rate minima value) \ (rate maxima value - rate minima value))) 
    
    Library: pandas
    Required files:
            - lungbroh_r.csv
            - femalebreast_r.csv
            - prostate_r.csv
            - colonandRectum_r.csv
            - pancrease_r.csv
            - liverandbillduct_r.csv
            - ovary_r.csv
            - eukemia_r.csv
            - nonhodgkinlymphoma_r.csv
            - corpus_r.csv
            
    Parameters
    ----------
    indication : int
        1. Female Breast Cancer (Top 2)
        2. Corpus and Uterus, NOS (Top 10)
        3. Ovary (Top 7)
        4. Prostate (Top 3)
        5. Lung and Bronchus Cancer (Top 1)
        6. Colon and Rectum (Top 4)
        7. Non-Hodgkin Lymphoma (Top 9)
        8. Leukemias (Top 8)
        9. Pancreas (Top 5)
        10. Liver (Top 6)

    gender : int
        Gender options:
        1. Male and Female
        2. Male only
        3. Female only
        
    race : int
        Race options:
        1. All Races and Ehnicities
        2. White
        3. Black
        4. American Indian and Alaska Native
        5. Asian and Pacific Islander
        6. Hispanic

    Returns
    -------
    cdc_f : dataframe 
       A dataframe containing final socring result of each state
    '''
    
    import pandas as pd
    
    # top 10 deadly cancer cleaned csv file name
    
    indication_to_csv = {
    5: "lungbroh_r.csv",
    1: "femalebreast_r.csv",
    4: "prostate_r.csv",
    6: "colonandRectum_r.csv",
    9: "pancrease_r.csv",
    10: "liverandbillduct_r.csv",
    3: "ovary_r.csv",
    8: "leukemia_r.csv",
    7: "nonhodgkinlymphoma_r.csv",
    2: "corpus_r.csv",}
    
    # To close warming message (https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas) 
    pd.options.mode.chained_assignment = None
    
    if indication in indication_to_csv:
        csv_filename = indication_to_csv[indication]
        # reads in csv
        cdc = pd.read_csv(csv_filename)     
        # selects rows matching gender and race
        cdc_sv = cdc.loc[(cdc["Sex_val"] == gender) & (cdc["Race_val"] == race)]
        # scores states by case counts (normalized)
        cdc_sv["CDC_Score"] = ((cdc_sv["Case Count"] - cdc_sv["Case Count"].min()) \
                            / (cdc_sv["Case Count"].max() - cdc_sv["Case Count"].min())*0.5) \
            + ((cdc_sv["Age-Adjusted Rate"] - cdc_sv["Age-Adjusted Rate"].min()) \
                / (cdc_sv["Age-Adjusted Rate"].max() - cdc_sv["Age-Adjusted Rate"].min())*0.5)
        # rounds scores
        cdc_sv["CDC_Score"] = cdc_sv["CDC_Score"].round(2)
        
        
        #weight the scores
        col=cdc_sv['CDC_Score'].apply(lambda x: 8 * x) 
        cdc_sv['CDC_Score'] = col 
        
        # sorts scores
        cdc_sv = cdc_sv.sort_values("CDC_Score", ascending = True)
        # selects state name column and score
        selected_columns = cdc_sv[["Area","CDC_Score"]]
        cdc_f = selected_columns.copy()
        # rename
        cdc_f.rename(columns={'Area' : 'State.Name'}, inplace=True)
        
        return cdc_f


