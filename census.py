# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:54:41 2021

@author: nunna
"""

# Team Snakes

import pandas as pd
import requests

# my key: 974cb90f79357696b2cfad1c9e471a279b3ee9ff
# Note: can include up to 50 api's

# https://api.census.gov/data/2019/acs/acs5/profile #html

# ACS 5 examples: https://api.census.gov/data/2019/acs/acs5/examples.html
# ACS 5 Variables: https://api.census.gov/data/2019/acs/acs5/variables.html


# 	https://api.census.gov/data/2019/acs/acs5?get=NAME,B01001_001E&for=county:*&key=YOUR_KEY_GOES_HERE

def census():
    """
    Libraries : pandas, requests
    
        This function accesses the ACS5 2019 CENSUS data for U.S. county population counts based on age and race/ethnicity.
    

    Returns
    -------
    census : pandas dataframe
        census contains aggregated and disaggreagted population counts by race/ethinicity and age for each county.
        
        Race/ethnicity groups include : white, Black, American Indian or Alaskan Native, Asian or Pacific Islander, Hispanic/Latino
        
        Age groups: child (<18 years), adult (18 to 64 years), older adult (65+ years)
        
        For each county, there is also a grand population total. 
        
        Note: The CENSUS API only allows for 50 variables per requests, so we had to run requests several times. The age variables 
        were not pre-grouped according to our age needs so we had to perform calculations to get our age groupings. We also were
        going to include additional racial groups but they did not match with CDC data, so the code is commented out.

    """
    age_list = ['B01001_001E',                  # total variable
                'B01001_003E','B01001_004E','B01001_005E','B01001_006E',        # child age variables
                'B01001_027E','B01001_028E','B01001_029E','B01001_030E',        
                'B01001_007E','B01001_008E','B01001_009E','B01001_010E','B01001_011E','B01001_012E',  # adult age variables
                'B01001_013E','B01001_014E','B01001_015E','B01001_016E','B01001_017E','B01001_018E',
                'B01001_019E','B01001_031E','B01001_032E','B01001_033E','B01001_034E','B01001_035E',
                'B01001_036E','B01001_037E','B01001_038E','B01001_039E','B01001_040E','B01001_041E',
                'B01001_042E','B01001_043E',
                'B01001_020E','B01001_021E','B01001_022E','B01001_023E','B01001_024E','B01001_025E',  # older adult age variables
                'B01001_044E','B01001_045E','B01001_046E','B01001_047E','B01001_048E','B01001_049E']
    
    wht_list = ['B01001A_001E',                 # total white pop variable
                'B01001A_003E','B01001A_004E','B01001A_005E','B01001A_006E',    # white child age variables
                'B01001A_018E','B01001A_019E','B01001A_020E','B01001A_021E',
                'B01001A_007E','B01001A_008E','B01001A_009E','B01001A_010E','B01001A_011E',     # white adult age variables
                'B01001A_012E','B01001A_013E','B01001A_022E','B01001A_023E','B01001A_024E',
                'B01001A_025E','B01001A_026E','B01001A_027E','B01001A_028E',
                'B01001A_014E','B01001A_015E','B01001A_016E',       # white older adult age variables
                'B01001A_029E','B01001A_030E','B01001A_031E']
    
    blk_list = ['B01001B_001E',                 # total black pop variable
                'B01001B_003E','B01001B_004E','B01001B_005E','B01001B_006E',    # black child age variables
                'B01001B_018E','B01001B_019E','B01001B_020E','B01001B_021E',
                'B01001B_007E','B01001B_008E','B01001B_009E','B01001B_010E','B01001B_011E',     # black adult age variable 
                'B01001B_012E','B01001B_013E','B01001B_022E','B01001B_023E','B01001B_024E',
                'B01001B_025E','B01001B_026E','B01001B_027E','B01001B_028E',
                'B01001B_014E','B01001B_015E','B01001B_016E',       # black older adult age variables
                'B01001B_029E','B01001B_030E','B01001B_031E']
    
    aak_list = ['B01001C_001E',                 # total AmInd.Ak pop variable
                'B01001C_003E','B01001C_004E','B01001C_005E','B01001C_006E',    # AmInd.Ak child age variables
                'B01001C_018E','B01001C_019E','B01001C_020E','B01001C_021E',
                'B01001C_007E','B01001C_008E','B01001C_009E','B01001C_010E','B01001C_011E',     # AmInd.Ak adult age variables
                'B01001C_012E','B01001C_013E','B01001C_022E','B01001C_023E','B01001C_024E',
                'B01001C_025E','B01001C_026E','B01001C_027E','B01001C_028E',
                'B01001C_014E','B01001C_015E','B01001C_016E',       # AmInd.Ak older adult age variables
                'B01001C_029E','B01001C_030E','B01001C_031E']
    
    asn_list = ['B01001D_001E',                 # Total asian pop variable
                'B01001D_003E','B01001D_004E','B01001D_005E','B01001D_006E',    # asian child age variables
                'B01001D_018E','B01001D_019E','B01001D_020E','B01001D_021E',
                'B01001D_007E','B01001D_008E','B01001D_009E','B01001D_010E','B01001D_011E',     # asian adult age variables
                'B01001D_012E','B01001D_013E','B01001D_022E','B01001D_023E','B01001D_024E',
                'B01001D_025E','B01001D_026E','B01001D_027E','B01001D_028E',
                'B01001D_014E','B01001D_015E','B01001D_016E',       # asian older adult age variables
                'B01001D_029E','B01001D_030E','B01001D_031E']
    
    pac_list = ['B01001E_001E',                 # Total PacIsl pop variable
                'B01001E_003E','B01001E_004E','B01001E_005E','B01001E_006E',    # PacIsl child age variables
                'B01001E_018E','B01001E_019E','B01001E_020E','B01001E_021E',    
                'B01001E_007E','B01001E_008E','B01001E_009E','B01001E_010E','B01001E_011E',     # PacIsl adult age variables
                'B01001E_012E','B01001E_013E','B01001E_022E','B01001E_023E','B01001E_024E',
                'B01001E_025E','B01001E_026E','B01001E_027E','B01001E_028E',
                'B01001E_014E','B01001E_015E','B01001E_016E',       # PacIsl older adult age variables
                'B01001E_029E','B01001E_030E','B01001E_031E']
    
    hsp_list = ['B01001I_001E',                 # Total hispanic pop variable
                'B01001I_003E','B01001I_004E','B01001I_005E','B01001I_006E',    # hispanic child age variables
                'B01001I_018E','B01001I_019E','B01001I_020E','B01001I_021E',    
                'B01001I_007E','B01001I_008E','B01001I_009E','B01001I_010E','B01001I_011E',     # hispanic adult age variables
                'B01001I_012E','B01001I_013E','B01001I_022E','B01001I_023E','B01001I_024E',
                'B01001I_025E','B01001I_026E','B01001I_027E','B01001I_028E',
                'B01001I_014E','B01001I_015E','B01001I_016E',       # PacIsl older adult age variables
                'B01001I_029E','B01001I_030E','B01001I_031E']
    
    # oth_list = ['B01001F_001E',                 # Total Other race pop variable
    #             'B01001F_003E','B01001F_004E','B01001F_005E','B01001F_006E',    # other child age variables
    #             'B01001F_018E','B01001F_019E','B01001F_020E','B01001F_021E',
    #             'B01001F_007E','B01001F_008E','B01001F_009E','B01001F_010E','B01001F_011E',     # other adult age variables
    #             'B01001F_012E','B01001F_013E','B01001F_022E','B01001F_023E','B01001F_024E',
    #             'B01001F_025E','B01001F_026E','B01001F_027E','B01001F_028E',
    #             'B01001F_014E','B01001F_015E','B01001F_016E',       # other older adult age variables
    #             'B01001F_029E','B01001F_030E','B01001F_031E']
    
    # two_list = ['B01001G_001E',                 # Total twomore race pop variable
    #             'B01001G_003E','B01001G_004E','B01001G_005E','B01001G_006E',    # twomore child age variables
    #             'B01001G_018E','B01001G_019E','B01001G_020E','B01001G_021E',
    #             'B01001G_007E','B01001G_008E','B01001G_009E','B01001G_010E','B01001G_011E',     # twomore adult age variables
    #             'B01001G_012E','B01001G_013E','B01001G_022E','B01001G_023E','B01001G_024E',
    #             'B01001G_025E','B01001G_026E','B01001G_027E','B01001G_028E',
    #             'B01001G_014E','B01001G_015E','B01001G_016E',       # twomore older adult age variables
    #             'B01001G_029E','B01001G_030E','B01001G_031E']
    
    
    
    # lists into strs for the API requests
    
    age_str = ','.join(age_list)
    wht_str = ','.join(wht_list)
    blk_str = ','.join(blk_list)
    aak_str = ','.join(aak_list)
    asn_str = ','.join(asn_list)
    pac_str = ','.join(pac_list)
    hsp_str = ','.join(hsp_list)
    # oth_str = ','.join(oth_list)
    # two_str = ','.join(two_list)
    
    
    
    ### REQUEST FOR AGE-ONLY GROUP POPULATIONS
    
    u1 = 'https://api.census.gov/data/2019/acs/acs5?get=NAME,'
    u2 = '&for=county:*&key=974cb90f79357696b2cfad1c9e471a279b3ee9ff'
    
    fullVars = age_str
    
    URL = u1 + fullVars + u2
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
    cols = data.pop(0)
    census = pd.DataFrame(data, columns = cols)
    
    # Change cols to numeric
    census = census.apply(pd.to_numeric, errors='ignore')
    
    # RENAME COLUMN
    census.rename(columns={'B01001_001E' : 'Total.Pop'}, inplace=True)
    
    
    ## CALCULATIONS TO FORM CHILD, ADULT, AND OLDER ADULT GROUPS
    
    # AGE POP
    # sum for age.child
    census['Total.Child.Pop'] = census[['B01001_003E','B01001_004E','B01001_005E','B01001_006E',
                'B01001_027E','B01001_028E','B01001_029E','B01001_030E']].sum(axis=1)
    # sum for age.adult
    census['Total.Adult.Pop'] = census[['B01001_007E','B01001_008E','B01001_009E','B01001_010E','B01001_011E','B01001_012E',
                'B01001_013E','B01001_014E','B01001_015E','B01001_016E','B01001_017E','B01001_018E',
                'B01001_019E','B01001_031E','B01001_032E','B01001_033E','B01001_034E','B01001_035E',
                'B01001_036E','B01001_037E','B01001_038E','B01001_039E','B01001_040E','B01001_041E',
                'B01001_042E','B01001_043E']].sum(axis=1)
    # sum for age.older
    census['Total.Older.Pop'] = census[['B01001_020E','B01001_021E','B01001_022E','B01001_023E','B01001_024E','B01001_025E',
                'B01001_044E','B01001_045E','B01001_046E','B01001_047E','B01001_048E','B01001_049E']].sum(axis=1)
    
    ## NEW DF
    selected_columns = census[['NAME','Total.Pop','Total.Child.Pop','Total.Adult.Pop','Total.Older.Pop']]
    age_df = selected_columns.copy()
    
    
    
    
    
    
    ### REQUEST FOR WHITE POPULATION GROUPS
    
    fullVars = wht_str
    
    URL = u1 + fullVars + u2
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
    cols = data.pop(0)
    census = pd.DataFrame(data, columns = cols)
    
    # Change cols to numeric
    census = census.apply(pd.to_numeric, errors='ignore')
    
    # RENAME COLUMN
    census.rename(columns={'B01001A_001E' : 'White.Pop'}, inplace=True)
    
    
    ## CALCULATIONS
    # sum for white child
    census['White.Child'] = census[['B01001A_003E','B01001A_004E','B01001A_005E','B01001A_006E',
                  'B01001A_018E','B01001A_019E','B01001A_020E','B01001A_021E']].sum(axis=1)
    # sum for white adult
    census['White.Adult'] = census[['B01001A_007E','B01001A_008E','B01001A_009E','B01001A_010E','B01001A_011E',
                  'B01001A_012E','B01001A_013E','B01001A_022E','B01001A_023E','B01001A_024E',
                  'B01001A_025E','B01001A_026E','B01001A_027E','B01001A_028E']].sum(axis=1)
    # sum for white older adult
    census['White.Older'] = census[['B01001A_014E','B01001A_015E','B01001A_016E',
                  'B01001A_029E','B01001A_030E','B01001A_031E']].sum(axis=1)
    
    ## NEW DF
    selected_columns = census[['White.Pop','White.Child','White.Adult','White.Older']]
    wht_df = selected_columns.copy()
    
    
    
    
    
    ### REQUEST FOR BLACK POP
    
    fullVars = blk_str
    
    URL = u1 + fullVars + u2
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
    cols = data.pop(0)
    census = pd.DataFrame(data, columns = cols)
    
    # Change cols to numeric
    census = census.apply(pd.to_numeric, errors='ignore')
    
    # RENAME COLUMN
    census.rename(columns={'B01001B_001E' : 'Black.Pop'}, inplace=True)
    
    
    ## CALCULATIONS
    # sum for black child
    census['Black.Child'] = census[['B01001B_003E','B01001B_004E','B01001B_005E','B01001B_006E',
                  'B01001B_018E','B01001B_019E','B01001B_020E','B01001B_021E']].sum(axis=1)
    # sum for black adult
    census['Black.Adult'] = census[['B01001B_007E','B01001B_008E','B01001B_009E','B01001B_010E','B01001B_011E',
                  'B01001B_012E','B01001B_013E','B01001B_022E','B01001B_023E','B01001B_024E',
                  'B01001B_025E','B01001B_026E','B01001B_027E','B01001B_028E']].sum(axis=1)
    # sum for black older adult
    census['Black.Older'] = census[['B01001B_014E','B01001B_015E','B01001B_016E',
                  'B01001B_029E','B01001B_030E','B01001B_031E']].sum(axis=1)
    
    ## NEW DF
    selected_columns = census[['Black.Pop','Black.Child','Black.Adult','Black.Older']]
    blk_df = selected_columns.copy()
    
    
    
    
    
    
    
    ### REQUEST FOR AMERICAN INDIAN OR ALASKAN NATIVE POP
    
    fullVars = aak_str
    
    URL = u1 + fullVars + u2
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
    cols = data.pop(0)
    census = pd.DataFrame(data, columns = cols)
    
    # Change cols to numeric
    census = census.apply(pd.to_numeric, errors='ignore')
    
    # RENAME COLUMN
    census.rename(columns={'B01001C_001E' : 'AmInd.Ak.Pop'}, inplace=True)
    
    # sum for AmIndAk child
    census['AmInd.Ak.Child'] = census[['B01001C_003E','B01001C_004E','B01001C_005E','B01001C_006E',
                  'B01001C_018E','B01001C_019E','B01001C_020E','B01001C_021E']].sum(axis=1)
    # sum for AmIndAk adult
    census['AmInd.Ak.Adult'] = census[['B01001C_007E','B01001C_008E','B01001C_009E','B01001C_010E','B01001C_011E',
                  'B01001C_012E','B01001C_013E','B01001C_022E','B01001C_023E','B01001C_024E',
                  'B01001C_025E','B01001C_026E','B01001C_027E','B01001C_028E']].sum(axis=1)
    # sum for AmIndAk older adult
    census['AmInd.Ak.Older'] = census[['B01001C_014E','B01001C_015E','B01001C_016E',
                  'B01001C_029E','B01001C_030E','B01001C_031E']].sum(axis=1)
    
    ## NEW DF
    selected_columns = census[['AmInd.Ak.Pop','AmInd.Ak.Child','AmInd.Ak.Adult','AmInd.Ak.Older']]
    aak_df = selected_columns.copy()
    
    
    
    
    
    
    ### ASIAN POP
    
    fullVars = asn_str
    
    URL = u1 + fullVars + u2
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
    cols = data.pop(0)
    census = pd.DataFrame(data, columns = cols)
    
    # Change cols to numeric
    census = census.apply(pd.to_numeric, errors='ignore')
    
    # RENAME COLUMN
    census.rename(columns={'B01001D_001E' : 'Asian.Pop'}, inplace=True)
    
    # sum for asian child
    census['Asian.Child'] = census[['B01001D_003E','B01001D_004E','B01001D_005E','B01001D_006E',
                  'B01001D_018E','B01001D_019E','B01001D_020E','B01001D_021E']].sum(axis=1)
    # sum for asian adult
    census['Asian.Adult'] = census[['B01001D_007E','B01001D_008E','B01001D_009E','B01001D_010E','B01001D_011E',
                  'B01001D_012E','B01001D_013E','B01001D_022E','B01001D_023E','B01001D_024E',
                  'B01001D_025E','B01001D_026E','B01001D_027E','B01001D_028E']].sum(axis=1)
    # sum for asian older adult
    census['Asian.Older'] = census[['B01001D_014E','B01001D_015E','B01001D_016E',
                  'B01001D_029E','B01001D_030E','B01001D_031E']].sum(axis=1)
    
    ## NEW DF
    selected_columns = census[['Asian.Pop','Asian.Child','Asian.Adult','Asian.Older']]
    asn_df = selected_columns.copy()
    
    
    
    
    
    
    ### PACIFIC ISLANDER POP
    
    fullVars = pac_str
    
    URL = u1 + fullVars + u2
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
    cols = data.pop(0)
    census = pd.DataFrame(data, columns = cols)
    
    # Change cols to numeric
    census = census.apply(pd.to_numeric, errors='ignore')
    
    # RENAME COLUMN
    census.rename(columns={'B01001E_001E' : 'PacIsl.Pop'}, inplace=True)
    
    # sum for PacIsl child
    census['PacIsl.Child'] = census[['B01001E_003E','B01001E_004E','B01001E_005E','B01001E_006E',
                  'B01001E_018E','B01001E_019E','B01001E_020E','B01001E_021E']].sum(axis=1)
    # sum for PacIsl adult
    census['PacIsl.Adult'] = census[['B01001E_007E','B01001E_008E','B01001E_009E','B01001E_010E','B01001E_011E',
                  'B01001E_012E','B01001E_013E','B01001E_022E','B01001E_023E','B01001E_024E',
                  'B01001E_025E','B01001E_026E','B01001E_027E','B01001E_028E']].sum(axis=1)
    # sum for PacIsl older adult
    census['PacIsl.Older'] = census[['B01001E_014E','B01001E_015E','B01001E_016E',
                  'B01001E_029E','B01001E_030E','B01001E_031E']].sum(axis=1)
    
    ## NEW DF
    selected_columns = census[['PacIsl.Pop','PacIsl.Child','PacIsl.Adult','PacIsl.Older']]
    pac_df = selected_columns.copy()
    
    ##
    ##
    ### COMBINE ASIAN AND PACIFIC ISLANDER INTO ONE GROUP TO MATCH CDC DATA
    ##
    ##
    
    combo = pd.concat([asn_df, pac_df], axis=1)
    # sum total
    combo['Asian.PacIsl.Pop'] = combo[['Asian.Pop', 'PacIsl.Pop']].sum(axis=1)
    # sum child
    combo['Asian.PacIsl.Child'] = combo[['Asian.Child', 'PacIsl.Child']].sum(axis=1)
    # sum adult
    combo['Asian.PacIsl.Adult'] = combo[['Asian.Adult', 'PacIsl.Adult']].sum(axis=1)
    # sum older adult
    combo['Asian.PacIsl.Older'] = combo[['Asian.Older', 'PacIsl.Older']].sum(axis=1)
    
    ## NEW DF
    selected_columns = combo[['Asian.PacIsl.Pop','Asian.PacIsl.Child','Asian.PacIsl.Adult','Asian.PacIsl.Older']]
    asp_df = selected_columns.copy()
    
    
    
    
    
    
    
    
    ### Hispanic POP
    
    fullVars = hsp_str
    
    URL = u1 + fullVars + u2
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
    
    cols = data.pop(0)
    census = pd.DataFrame(data, columns = cols)
    
    
    # Change cols to numeric (DIFFERENT FOR THIS LAST SET -- to keep state and county as str's)
    cols=[i for i in census.columns if i not in ['NAME','state','county']]
    for col in cols:
        census[col]=pd.to_numeric(census[col])
    
    # RENAME COLUMN
    census.rename(columns={'B01001I_001E' : 'Hispanic.Pop',
                           'state' : 'State.ID',
                           'county' : 'County.ID'}, inplace=True)
    
    # sum for PacIsl child
    census['Hispanic.Child'] = census[['B01001I_003E','B01001I_004E','B01001I_005E','B01001I_006E',
                  'B01001I_018E','B01001I_019E','B01001I_020E','B01001I_021E']].sum(axis=1)
    # sum for PacIsl adult
    census['Hispanic.Adult'] = census[['B01001I_007E','B01001I_008E','B01001I_009E','B01001I_010E','B01001I_011E',
                  'B01001I_012E','B01001I_013E','B01001I_022E','B01001I_023E','B01001I_024E',
                  'B01001I_025E','B01001I_026E','B01001I_027E','B01001I_028E']].sum(axis=1)
    # sum for PacIsl older adult
    census['Hispanic.Older'] = census[['B01001I_014E','B01001I_015E','B01001I_016E',
                  'B01001I_029E','B01001I_030E','B01001I_031E']].sum(axis=1)
    
    ## NEW DF
    selected_columns = census[['Hispanic.Pop','Hispanic.Child','Hispanic.Adult','Hispanic.Older',
                               'State.ID', 'County.ID']]
    hsp_df = selected_columns.copy()
    
    
    
    
    
    
    ### OTHER POP
    
    # fullVars = oth_str
    
    # URL = u1 + fullVars + u2
    # response = requests.get(URL)
    # if response.status_code == 200:
    #     data = response.json()
    
    # cols = data.pop(0)
    # census = pd.DataFrame(data, columns = cols)
    
    # # Change cols to numeric
    # census = census.apply(pd.to_numeric, errors='ignore')
    
    # # RENAME COLUMN
    # census.rename(columns={'B01001F_001E' : 'Other.Pop'}, inplace=True)
    
    # # sum for other child
    # census['Other.Child'] = census[['B01001F_003E','B01001F_004E','B01001F_005E','B01001F_006E',
    #               'B01001F_018E','B01001F_019E','B01001F_020E','B01001F_021E']].sum(axis=1)
    # # sum for other adult
    # census['Other.Adult'] = census[['B01001F_007E','B01001F_008E','B01001F_009E','B01001F_010E','B01001F_011E',
    #               'B01001F_012E','B01001F_013E','B01001F_022E','B01001F_023E','B01001F_024E',
    #               'B01001F_025E','B01001F_026E','B01001F_027E','B01001F_028E']].sum(axis=1)
    # # sum for other older adult
    # census['Other.Older'] = census[['B01001F_014E','B01001F_015E','B01001F_016E',
    #               'B01001F_029E','B01001F_030E','B01001F_031E']].sum(axis=1)
    
    # ## NEW DF
    # selected_columns = census[['Other.Pop','Other.Child','Other.Adult','Other.Older']]
    # oth_df = selected_columns.copy()
    
    
    
    
    
    ### TWOMORE POP
    
    # fullVars = two_str
    
    # URL = u1 + fullVars + u2
    # response = requests.get(URL)
    # if response.status_code == 200:
    #     data = response.json()
    
    # cols = data.pop(0)
    # census = pd.DataFrame(data, columns = cols)
    
    # # Change cols to numeric (DIFFERENT FOR THIS LAST SET -- to keep state and county as str's)
    # cols=[i for i in census.columns if i not in ['NAME','state','county']]
    # for col in cols:
    #     census[col]=pd.to_numeric(census[col])
    
    
    
    # # RENAME COLUMN
    # census.rename(columns={'B01001G_001E' : 'TwoMore.Pop'}, inplace=True)
    
    # # sum for twomore child
    # census['TwoMore.Child'] = census[['B01001G_003E','B01001G_004E','B01001G_005E','B01001G_006E',
    #               'B01001G_018E','B01001G_019E','B01001G_020E','B01001G_021E']].sum(axis=1)
    # # sum for twomore adult
    # census['TwoMore.Adult'] = census[['B01001G_007E','B01001G_008E','B01001G_009E','B01001G_010E','B01001G_011E',
    #               'B01001G_012E','B01001G_013E','B01001G_022E','B01001G_023E','B01001G_024E',
    #               'B01001G_025E','B01001G_026E','B01001G_027E','B01001G_028E']].sum(axis=1)
    # # sum for twomore older adult
    # census['TwoMore.Older'] = census[['B01001G_014E','B01001G_015E','B01001G_016E',
    #               'B01001G_029E','B01001G_030E','B01001G_031E']].sum(axis=1)
    
    # ## NEW DF
    # selected_columns = census[['TwoMore.Pop','TwoMore.Child','TwoMore.Adult','TwoMore.Older',
    #                            'state', 'county']]
    # two_df = selected_columns.copy()
    
    
    
    
    
    
    
    
    
    ## CONCAT ALL THE DATAFRAMES
    df = pd.concat([age_df, wht_df, blk_df, aak_df, asp_df, hsp_df], axis=1)
    
    
    
    ## Add COUNTYFIPS COLUMN : FOR MERGING WITH HOSPITAL DATASET
    df['COUNTYFIPS'] = df['State.ID'] + df['County.ID']
    
    
    
    ## FUNCTION TO ADD STATENAME COLUMN: FOR MERGING WITH THE CDC DATASET
    def extract_state(a):
        """
        Takes a str and splits it on the comma.
        Then takes the index 0 value and strips it of the left white space.

        Parameters
        ----------
        a : STR

        Returns
        -------
        state_name : str
            The second word in a "Word, Word" pair.

        """
        asplit = a.split(",")
        state_name = asplit[1].lstrip()
        return state_name
    
    ## APPLY EXTRACT STATE FUNCTION ON CENSUS NAME COLUMN THAT CONTAINS "COUNTY, STATE" STR VALUES
    # AND JOINS WITH CENSUS TABLE
    census = df.join(df['NAME'].apply(lambda x: pd.Series(extract_state(x),
                                                  index=['State.Name'])))
    return census



    
















### HOSPITAL DATA 

#hospitals = pd.read_csv('Hospitals.csv')


# [['ID','NAME','ADDRESS','CITY','STATE','ZIP','TELEPHONE','POPULATION','COUNTY',
#   'COUNTYFIPS',]]
# for joining



# # NEW DF
# selected_columns = census[['NAME','Total.Pop', 'White.Pop','Black.Pop','AmInd.Ak.Pop',
#                            'Asian.Pop', 'PacIsl.Pop', 'Other.Pop','TwoMore.Pop',
#                            'Total.Child.Pop','Total.Adult.Pop','Total.Older.Pop',
#                            'White.Child','White.Adult','White.Older',
#                            'Black.Child','Black.Adult','Black.Older',
#                            'AmInd.Ak.Child','AmInd.Ak.Adult','AmInd.Ak.Older',
#                            'Asian.Child','Asian.Adult','Asian.Older',
#                            'PacIsl.Child','PacIsl.Adult','PacIsl.Older',
#                            'Other.Child','Other.Adult','Other.Older',
#                            'TwoMore.Child','TwoMore.Adult','TwoMore.Older']]

# census.df = selected_columns.copy()





















 
