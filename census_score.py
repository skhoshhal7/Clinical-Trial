# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 23:47:24 2021

@author: nunna
"""
# census_score.py


import pandas as pd

def census_score(census, age, race, condition):
    """
    This function provides a score to each county based off the age, race, and condition
    selection of the user. 
    
    A specific county population column is selected by the age and race input of the user.
        EX: if 'white' and '<18 years' of age is chosen, the census column 'White.Child'
        will be chosen.
    
    The selected county population column is scored using the scorer() function below.


    Parameters
    ----------
    census : dataframe
        The county census dataframe returned from census.py
    age : int
        An int from 0-3 that represents the age grouping the user chooses in script.py
    race : int
        An int from 0-5 that represents the race/ethnicity grouping the user chooses in script.py
    condition : int
        An int from 0-9 that represents the cancer type the user chooses in script.py

    Returns
    -------
    Dateframe
        A dataframe with 'County, State' name, state name, COUNTYFIPS, and newly added census score.

    """
    # Cancer rates per 100k people
    # https://gis.cdc.gov/Cancer/USCS/#/AtAGlance/
    n = 100000
    breast_r = 127      # women only
    uterus_r = 27       # women only
    ovary_r = 10        # women only
    prostate_r = 108    # men only
    lung_r = 54
    colon_r = 37
    non_hodg_r = 18
    leukemia_r = 13
    pancreas_r = 13
    liver_r = 8
    
    # list of rate variables
    c_list = [breast_r, uterus_r, ovary_r, prostate_r, lung_r,
              colon_r, non_hodg_r, leukemia_r, pancreas_r, liver_r]
    
    # finds 1 cancer case rate (i.e 1 per 500 people)
    pop_rate = []
    for c in c_list:
        pop_rate.append(round(n / c, 0))
    
    # get's pop needed for 20 to 80 participants based of rate above
    trial_pop = []
    trial_size = range(20,81)
    for i in range(len(pop_rate)):
        pop_size = []
        for s in trial_size:
            pop_size.append(pop_rate[i] * s)
        trial_pop.append(pop_size)
        
    
    col_names = ['Female Breast Cancer',
                 'Corpus and Uterus, NOS',
                 'Ovary',
                 'Prostate',
                 'Lung and Bronchus Cancer',
                 'Colon and Rectum',
                 'Non-Hodgkin Lymphoma',
                 'Leukemias',
                 'Pancreas',
                 'Liver']
    
    # dataframe of cancers and pop needed 
    pop_rate_df = pd.DataFrame()
    for i in range(len(trial_pop)):
        pop_rate_df[col_names[i]] = trial_pop[i]
    
    
    # Add number of participants column
    pop_rate_df.insert(0, 'Participant Count', range(20,81))
    
    # Pull every 6th row (up to 10 points based on population)
    df1 = pop_rate_df[pop_rate_df.index % 6 == 0]
    
    
    
    param_list = [['Total.Child.Pop','White.Child','Black.Child','AmInd.Ak.Child','Asian.PacIsl.Child','Hispanic.Child'],
                  ['Total.Adult.Pop','White.Adult','Black.Adult','AmInd.Ak.Adult','Asian.PacIsl.Adult','Hispanic.Adult'],
                  ['Total.Older.Pop','White.Older','Black.Older','AmInd.Ak.Older','Asian.PacIsl.Older','Hispanic.Older'],
                  ['Total.Pop','White.Pop','Black.Pop','AmInd.Ak.Pop','Asian.PacIsl.Pop','Hispanic.Pop']]
    
    # parameter DF
    parameter_df = pd.DataFrame(param_list)
    
    # score each column
    parameter = parameter_df.iloc[age - 1][race - 1]
    cond = col_names[condition - 1]
    
    def scorer(x):
        """
        Scoring criteria:
        - First round clinical trials average between 20 to 80 participants
        - Each cancer type has a rate of new singular cases (i.e. 1 new lung cancer case per 12500 people)
        - For a county to be likely to have 20 cancer participants, it must have a population of
            at least 20 * (the denominator of the rate of new singular cases) 
            - The participant range of 20-80 is divided into 11 buckets of populations
            - Each county will fall in one of the buckets and receive a score from 0 to 1,
                incremented by 0.1 (The larger buckets receiving the highest score)
                - EX: if a county meets the minimum population needed for the likely hood of
                    80 participants, then it would recieve a score of 1
        - The county population that is scored against the buckets is determined by the
            age and race the user selected. Only the resulting column will used for scoring.
            - 

        Parameters
        ----------
        x : Dataframe column value
            The population of a subgroup of a county.

        Returns
        -------
        numeric
            A score from 0 to 1 (incremented by 0.1)

        """
        if cond in ['Female Breast Cancer',
                         'Corpus and Uterus, NOS',
                         'Ovary',
                         'Prostate']:
            if x / 2 >= df1.iloc[9][cond]:
                return 1
            elif x / 2 >= df1.iloc[8][cond]:
                return 0.9
            elif x / 2 >= df1.iloc[7][cond]:
                return 0.8
            elif x / 2 >= df1.iloc[6][cond]:
                return 0.7
            elif x / 2 >= df1.iloc[5][cond]:
                return 0.6
            elif x / 2 >= df1.iloc[4][cond]:
                return 0.5
            elif x / 2 >= df1.iloc[3][cond]:
                return 0.4
            elif x / 2 >= df1.iloc[2][cond]:
                return 0.3
            elif x / 2 >= df1.iloc[1][cond]:
                return 0.2
            elif x / 2 >= df1.iloc[0][cond]:
                return 0.1
            else:
                return 0
        else:    
            if x >= df1.iloc[9][cond]:
                return 1
            elif x >= df1.iloc[8][cond]:
                return 0.9
            elif x >= df1.iloc[7][cond]:
                return 0.8
            elif x >= df1.iloc[6][cond]:
                return 0.7
            elif x >= df1.iloc[5][cond]:
                return 0.6
            elif x >= df1.iloc[4][cond]:
                return 0.5
            elif x >= df1.iloc[3][cond]:
                return 0.4
            elif x >= df1.iloc[2][cond]:
                return 0.3
            elif x >= df1.iloc[1][cond]:
                return 0.2
            elif x >= df1.iloc[0][cond]:
                return 0.1
            else:
                return 0
    
    
    census['Census_Score'] = census[parameter].apply(scorer)
    
    # WEIGHT THE SCORE
    col=census['Census_Score'].apply(lambda x: 8 * x) 
    census['Census_Score'] = col 
    
    selected_columns = census[['NAME','State.Name','COUNTYFIPS','Census_Score']]
    
    df = selected_columns.copy()
    
    df.rename(columns={'NAME' : 'County.State'}, inplace=True)
    
    return df