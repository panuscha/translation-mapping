import pandas as pd
import math

def save_to_dict(countries, map_year, df_dict, row):
    for country in countries:
                key = (country, map_year) 
                if key in df_dict:
                    df_dict[key] += row['weight']   
                else:
                    df_dict[key] =  row['weight']

#geotagged_df = pd.read_csv("geotagged/geotagged_germany_country_update.csv")
geotagged_df = pd.read_excel("geotagged/geotagged_germany_country_update.xlsx")


plot_years = [1945, 1956, 1967, 1978, 1989, 2000, 2011] 
df_dict = {}

for plot_year in plot_years:     
    for _, row in geotagged_df[(geotagged_df['year'] >= plot_year) & (geotagged_df['year'] < plot_year + 11)].iterrows():
        
        # GERMAN
        german_speaking = row['geonames_country'] == 'Austria' or row['geonames_country'] == 'Switzerland' or  row['geonames_country'] == 'Liechtenstein'
        german_language = row['language'] == 'ger'
        
        # FRENCH
        french_speaking = row['geonames_country'] == 'France' or row['geonames_country'] == 'Switzerland' or row['geonames_country'] == 'Belgium' or row['geonames_country'] == 'Monaco' or row['geonames_country'] == 'Luxembourg'
        french_language = row['language'] == 'fre'
        french_countries = ['France', 'Switzerland fre', 'Belgium fre', 'Monaco', 'Luxembourg']
        french_cond = french_language and french_speaking

        # DUTCH
        dutch_speaking = row['geonames_country'] == 'Belgium' or row['geonames_country'] == 'Netherlands'
        dutch_language = row['language'] == 'dut'
        dutch_countries = ['Belgium dut', 'Netherlands']
        dutch_cond = dutch_language and dutch_speaking

        # ITALIAN
        italian_speaking = row['geonames_country'] == 'Switzerland' or row['geonames_country'] == 'Italy'
        italian_language = row['language'] == 'ita'
        italian_countries = ['Switzerland ita', 'Italy']
        italian_cond = italian_language and italian_speaking

        # SERBO CROATIAN
        serbo_croatian_speaking = (row['geonames_country'] == 'Croatia' or row['geonames_country'] == 'Bosnia and Herzegovina' or  
                                   row['geonames_country'] == 'Serbia' or  row['geonames_country'] == 'Montenegro')
        serbo_croatian_language = row['language'] == 'hrv' or row['language'] == 'srp' or row['language'] == 'bos'
        serbo_croatian_cond = serbo_croatian_language and serbo_croatian_speaking
        serbo_croatian_countries = ['Croatia', 'Bosnia and Herzegovina', 'Serbia', 'Montenegro']

        # ENGLISH
        english_speaking = row['geonames_country'] == 'United Kingdom' or row['geonames_country'] == 'Ireland'
        english_language = row['language'] == 'eng'
        english_cond = english_language and english_speaking
        english_countries = ['United Kingdom', 'Ireland']

        # SWISS
        swiss_cond = row['geonames_country'] == 'Switzerland'
        swiss_countries = ['Switzerland ita', 'Switzerland fre', 'Switzerland ger']

        # BELGIAN
        belgian_cond = row['geonames_country'] == 'Belgium'
        belgian_countries = ['Belgium dut', 'Belgium fre']

        # HUNGARY
        hungary_speaking = row['geonames_country'] == 'Slovakia' or row['geonames_country'] == 'Hungary'
        hungary_language  = row['language'] == 'hun'
        hungary_cond = hungary_language and hungary_speaking
        hungary_countries = ['Hungary']

        # SPAIN AND CATALONIA
        spanish_speaking =  row['geonames_country'] == 'Spain' or row['geonames_country'] == 'Catalonia'
        spanish_language = row['language'] == 'spa'
        spanish_cond = spanish_language and spanish_speaking
        spanish_countries = ['Spain', 'Catalonia']     
        
        # ROMANIA AND MOLDOVA
        romanian_speaking = row['geonames_country'] == 'Romania' or row['geonames_country'] == 'Moldova'
        romanian_language = row['language'] == 'rum'   

        # ARABIC
        arabic_speaking = row['language'] == 'ara'   


        if plot_year < 1989:
            german_cond = german_language and (row['region_country_name'] == 'West Germany' or german_speaking) 
            german_countries = ['West Germany', 'Austria', 'Switzerland ger',  'Liechtenstein'] 

            germany_rest_cond = False

            # SOVIET
            russian_speaking =  (row['geonames_country'] == 'Estonia' or row['geonames_country'] == 'Lithuania' or  row['geonames_country'] == 'Latvia' or  
                                 row['geonames_country'] == 'Byelarus' or row['geonames_country'] == 'Ukraine' or row['geonames_country'] == 'Moldova' or
                                 row['geonames_country'] == 'Russia' or row['geonames_country'] == 'Georgia' or row['geonames_country'] == 'Azerbaijan' or 
                                 row['geonames_country'] == 'Armenia' or row['geonames_country'] == 'Kazakhstan' or row['geonames_country'] == 'Turkmenistan' or
                                 row['geonames_country']  == 'Uzbekistan')
            russian_language = row['language'] == 'rus'
            soviet_cond = russian_language and russian_speaking
            soviet_countries = ['Estonia', 'Lithuania', 'Latvia', 'Byelarus', 'Ukraine', 'Moldova', 'Russia', 'Georgia', 'Azerbaijan', 'Armenia', 'Kazakhstan', 'Turkmenistan', 'Uzbekistan'   ]

            # YUGOSLAVIA 
            serbo_croatian_countries.extend(['Slovenia', 'Macedonia'])    
            
            romanian_cond = False   


            # CZECHOSLOVAKIA
                 

        else:
            german_cond = german_language and (row['geonames_country'] == 'Germany' or german_speaking)
            german_countries = ['West Germany', 'East Germany', 'Austria', 'Switzerland ger',  'Liechtenstein'] 

            germany_rest_cond = row['geonames_country'] == 'Germany'
            soviet_cond = False   
            
            romanian_cond = romanian_language and romanian_speaking
            romanian_countries = ['Romania', 'Moldova']
            
            
        
        ##### GERMAN SPEAKING ##### 

        if german_cond:
            save_to_dict(german_countries, plot_year, df_dict, row)  
            continue

        if germany_rest_cond:
            save_to_dict(['West Germany', 'East Germany'], plot_year, df_dict, row)
            continue

        ##### FRENCH SPEAKING ##### 

        if french_cond:
            save_to_dict(french_countries, plot_year, df_dict, row)  
            continue

        ##### ITALIAN SPEAKING ##### 

        if italian_cond:
            save_to_dict(italian_countries, plot_year, df_dict, row)  
            continue

        ##### DUTCH SPEAKING ##### 
        
        if dutch_cond:
            save_to_dict(dutch_countries, plot_year, df_dict, row)
            continue
        
        ##### SWITZERLAND ##### 

        if swiss_cond:
            save_to_dict(swiss_countries, plot_year, df_dict, row)  
            continue

        ##### BELGIUM ##### 

        if belgian_cond:
            save_to_dict(belgian_countries, plot_year, df_dict, row)  
            continue
        
        ##### SERBO-CROATIAN SPEAKING #####         

        if serbo_croatian_cond:
            save_to_dict(serbo_croatian_countries, plot_year, df_dict, row)     
            continue  

        ##### HUNGARIAN SPEAKING ##### 

        if hungary_cond:
            save_to_dict(hungary_countries, plot_year, df_dict, row)  
            continue           

        ##### UK AND IRELAND  #####

        if english_cond:
            save_to_dict(english_countries, plot_year, df_dict, row)  
            continue

        ##### SPANISH #####

        if spanish_cond:
            save_to_dict(spanish_countries, plot_year, df_dict, row)  
            continue

        #### SOVIET ####

        if soviet_cond:
            save_to_dict(soviet_countries, plot_year, df_dict, row)    
            continue
        
        #### ROMANIA ####

        if romanian_cond:
            save_to_dict(romanian_countries, plot_year, df_dict, row)    
            continue


        ##### ARABIC ####

        if arabic_speaking:
            save_to_dict(['Algeria', 'Tunisia', 'Syria'], plot_year, df_dict, row)
            continue

        ##### ALBANIA ####

        if row['language'] == 'alb':
            save_to_dict(['Albania'], plot_year, df_dict, row)    
            continue  



        ##### REST ####  means + everything written in the country !

        key = (row['region_country_name'], plot_year) 
        if key in df_dict:
            df_dict[key] += row['weight']
        else:
            df_dict[key] =  row['weight']

            

#df = pd.DataFrame.from_dict(list(df_dict), columns=['country','map_year']).assign(weights=df_dict.values())

df = pd.Series(df_dict).reset_index()   
df.columns = ['country', 'map_year', 'weights'] 
#df['weights'] = df['weights'].apply(lambda x: math.log2(x))
df.to_csv('weights/weights_language_families.csv')            
        

        
                      

