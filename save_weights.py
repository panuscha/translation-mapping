import pandas as pd
import numpy as np

folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/"

geotagged_df = pd.read_csv("geotagged/geotagged_lang_hist_country_new.csv")

map_years = np.unique(geotagged_df['map_year']) 
df_dict = {}

for map_year in map_years:
    for _, row in geotagged_df[geotagged_df['map_year'] == map_year]:

        ##### GERMAN SPEAKING #####
        
        if row['geonames_country'] == 'Germany':
            if row['language'] == 'ger':
                for country in ['Germany', 'Austria', 'Switzerland ger',  'Liechtenstein']:
                    key = (country, map_year)
                    if key in df_dict:
                        df_dict[key] = row['weight']    
                    else:
                        df_dict[key] = + row['weight']
            else:
                key = (row['geonames_country'], map_year)
                df_dict[key] = row['weight'] 

        if row['geonames_country'] == 'Austria':
            if row['language'] == 'ger':
                for country in ['Germany', 'Austria', 'Switzerland ger',  'Liechtenstein']:
                    key = (country, map_year)
                    if key in df_dict:
                        df_dict[key] = row['weight']    
                    else:
                        df_dict[key] = + row['weight']
            else:
                key = (row['geonames_country'], map_year)
                df_dict[key] = row['weight']        

        if row['geonames_country'] == 'Switzerland':
            if row['language'] == 'ger':
                for country in ['Germany', 'Austria', 'Switzerland ger',  'Liechtenstein']:
                    key = (country, map_year)
                    if key in df_dict:
                        df_dict[key] = row['weight']    
                    else:
                        df_dict[key] = + row['weight']
            else:
                for part in ['Switzerland ger', 'Switzerland fre']:
                    key = (row['geonames_country'], map_year)
                    df_dict[key] = row['weight']

        if row['geonames_country'] == 'Liechtenstein':
            if row['language'] == 'ger':
                for country in ['Germany', 'Austria', 'Switzerland ger',  'Liechtenstein']:
                    key = (country, map_year)
                    if key in df_dict:
                        df_dict[key] = row['weight']    
                    else:
                        df_dict[key] = + row['weight']
            else:
                key = (row['geonames_country'], map_year)
                df_dict[key] = row['weight']        

        ##### SERBO-CROATIAN SPEAKING ####         

        if row['geonames_country'] == 'Croatia': # row['geonames_country'] == 'Bosnia and Herzegovina' or row['geonames_country'] == 'Serbia')
            if (row['language'] == 'hrv' or row['language'] == 'srp' or row['language'] == 'bos') :
                for country in ['Croatia', 'Bosnia and Herzegovina', 'Serbia']:
                    key = (country, map_year) 
                    if key in df_dict:
                        df_dict[key] = row['weight']    
                    else:
                        df_dict[key] = + row['weight'] 
                else:
                    key = (row['geonames_country'], map_year)
                    df_dict[key] = row['weight'] 

        if row['geonames_country'] == 'Bosnia and Herzegovina': # row['geonames_country'] == 'Bosnia and Herzegovina' or row['geonames_country'] == 'Serbia')
            if (row['language'] == 'hrv' or row['language'] == 'srp' or row['language'] == 'bos') :
                for country in ['Croatia', 'Bosnia and Herzegovina', 'Serbia']:
                    key = (country, map_year) 
                    if key in df_dict:
                        df_dict[key] = row['weight']    
                    else:
                        df_dict[key] = + row['weight'] 
                else:
                    key = (row['geonames_country'], map_year)
                    df_dict[key] = row['weight']  

        if row['geonames_country'] == 'Serbia': # row['geonames_country'] == 'Bosnia and Herzegovina' or row['geonames_country'] == 'Serbia')
            if (row['language'] == 'hrv' or row['language'] == 'srp' or row['language'] == 'bos') :
                for country in ['Croatia', 'Bosnia and Herzegovina', 'Serbia']:
                    key = (country, map_year) 
                    if key in df_dict:
                        df_dict[key] = row['weight']    
                    else:
                        df_dict[key] = + row['weight'] 
                else:
                    key = (row['geonames_country'], map_year)
                    df_dict[key] = row['weight']                       

        ##### FRENCH SPEAKING #### 

        if row['language'] == 'fre' and (row['geonames_country'] == 'France' or row['geonames_country'] == 'Switzerland' or row['geonames_country'] == 'Belgium' or row['geonames_country'] == 'Monaco'):
            for country in ['France', 'Switzerland fre', 'Belgium fre', 'Monaco']:
                key = (country, map_year) 
                if key in df_dict:
                    df_dict[key] = row['weight']    
                else:
                    df_dict[key] = + row['weight']

        


        if row['language'] == 'fre' and (row['geonames_country'] == 'Canada'):
            key = ("Canada fre", map_year)
            if key in df_dict:
                df_dict[key] = row['weight']    
            else:
                df_dict[key] = + row['weight']                        
        if row['language'] == 'dut' and (row['geonames_country'] == 'Belgium' and row['geonames_country'] == 'Netherlands'):
            for country in ['Belgium dut', 'Netherlands']:
                key = (country, map_year)
                if key in df_dict:
                    df_dict[key] = row['weight']    
                else:
                    df_dict[key] = + row['weight']
