import pandas as pd

def save_to_dict(countries, map_year, df_dict, row):
    for country in countries:
                key = (country, map_year) 
                if key in df_dict:
                    df_dict[key] += row['weight']    
                else:
                    df_dict[key] =  row['weight'] 

#geotagged_df = pd.read_csv("geotagged/geotagged_germany_country_update.csv")
geotagged_df = pd.read_excel("geotagged/geotagged_germany_country_update.xlsx")


map_years = [1945, 1960, 1994, 2000] 
df_dict = {}

for map_year in map_years:
    for _, row in geotagged_df[geotagged_df['map_year'] == map_year].iterrows():
        
        german_speaking = row['geonames_country'] == 'Austria' or row['geonames_country'] == 'Switzerland' or  row['geonames_country'] == 'Liechtenstein'
        german_language = row['language'] == 'ger'
        
        french_speaking = row['geonames_country'] == 'France' or row['geonames_country'] == 'Switzerland' or row['geonames_country'] == 'Belgium' or row['geonames_country'] == 'Monaco'
        french_language = row['language'] == 'fre'
        french_countries = ['France', 'Switzerland fre', 'Belgium fre', 'Monaco']
        french_cond = french_language and french_speaking

        dutch_speaking = row['geonames_country'] == 'Belgium' or row['geonames_country'] == 'Netherlands'
        dutch_language = row['language'] == 'dut'
        dutch_countries = ['Belgium dut', 'Netherlands']
        dutch_cond = dutch_language and dutch_speaking

        italian_speaking = row['geonames_country'] == 'Switzerland' or row['geonames_country'] == 'Italy'
        italian_language = row['language'] == 'ita'
        italian_countries = ['Switzerland ita', 'Italy']
        italian_cond = italian_language and italian_speaking

        serbo_croatian_speaking = row['geonames_country'] == 'Croatia' or row['geonames_country'] == 'Bosnia and Herzegovina' or  row['geonames_country'] == 'Serbia' or  row['geonames_country'] == 'Montenegro'
        serbo_croatian_language = row['language'] == 'hrv' or row['language'] == 'srp' or row['language'] == 'bos'
        serbo_croatian_cond = serbo_croatian_language and serbo_croatian_speaking
        serbo_croatian_countries = ['Croatia', 'Bosnia and Herzegovina', 'Serbia', 'Montenegro']

        swiss_cond = row['geonames_country'] == 'Switzerland'
        swiss_countries = ['Switzerland ita', 'Switzerland fre', 'Switzerland ger']

        belgian_cond = row['geonames_country'] == 'Belgium'
        belgian_countries = ['Belgium dut', 'Belgium fre']



        if map_year < 1994:
            german_cond = german_language and (row['region_country_name'] == 'West Germany' or german_speaking) 
            german_countries = ['West Germany', 'Austria', 'Switzerland ger',  'Liechtenstein'] 

            germany_rest_cond = False

        else:
            german_cond = german_language and (row['geonames_country'] == 'Germany' or german_speaking)
            german_countries = ['West Germany', 'East Germany', 'Austria', 'Switzerland ger',  'Liechtenstein'] 

            germany_rest_cond = row['geonames_country'] == 'Germany'  
        
        ##### GERMAN SPEAKING ##### 

        if german_cond:
            save_to_dict(german_countries, map_year, df_dict, row)  
            continue

        if germany_rest_cond:
            save_to_dict(['West Germany', 'East Germany'], map_year, df_dict, row)
            continue

        ##### FRENCH SPEAKING #### 

        if french_cond:
            save_to_dict(french_countries, map_year, df_dict, row)  
            continue

        ##### ITALIAN SPEAKING #### 

        if italian_cond:
            save_to_dict(italian_countries, map_year, df_dict, row)  
            continue

        ##### DUTCH SPEAKING #### 
        
        if dutch_cond:
            save_to_dict(dutch_countries, map_year, df_dict, row)
            continue
        
        ##### SWITZERLAND #### 

        if swiss_cond:
            save_to_dict(swiss_countries, map_year, df_dict, row)  
            continue

        ##### BELGIUM #### 

        if belgian_cond:
            save_to_dict(belgian_countries, map_year, df_dict, row)  
            continue
        
        ##### SERBO-CROATIAN SPEAKING ####         

        if serbo_croatian_cond:
            if map_year < 1994:
                save_to_dict(serbo_croatian_countries, map_year, df_dict, row)
            else:
                save_to_dict(serbo_croatian_countries, map_year, df_dict, row)     
            continue  

        ##### HUNGARIAN SPEAKING #### 

        if row['language'] == 'hun':
            save_to_dict(['Hungary'], map_year, df_dict, row)            

        ##### REST #### 

        key = (row['region_country_name'], map_year) 
        if key in df_dict:
            df_dict[key] += row['weight']    
        else:
            df_dict[key] =  row['weight']  

            

#df = pd.DataFrame.from_dict(list(df_dict), columns=['country','map_year']).assign(weights=df_dict.values())

df = pd.Series(df_dict).reset_index()   
df.columns = ['country', 'map_year', 'weights'] 
df.to_csv('weights/weights_language_families.csv')            
        

        
                      

