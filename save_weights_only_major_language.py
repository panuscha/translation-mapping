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

        # HUNGARY
        hungary_speaking =  row['geonames_country'] == 'Hungary' #row['geonames_country'] == 'Slovakia' or
        hungary_language  = row['language'] == 'hun'
        hungary_cond = hungary_language and hungary_speaking
        hungary_countries = ['Hungary']

        # SPAIN AND CATALONIA
        spanish_speaking =  row['geonames_country'] == 'Spain' #or row['geonames_country'] == 'Catalonia'
        spanish_language = row['language'] == 'spa'
        spanish_cond = spanish_language and spanish_speaking
        spanish_countries = ['Spain'] #, 'Catalonia'   

        # ROMANIA AND MOLDOVA
        romanian_speaking = row['geonames_country'] == 'Romania' or row['geonames_country'] == 'Moldova'
        romanian_language = row['language'] == 'rum'
        romanian_cond = romanian_speaking and romanian_language
        romanian_countries = ['Romania', 'Moldova']    

        # SLOVENIAN
        slovenian_language = row['language'] == 'slv' and row['geonames_country'] == 'Slovenia'
    
        # POLISH
        polish_language = row['language'] == 'pol' and row['geonames_country'] == 'Poland'

        # DANISH
        danish_language = row['language'] == 'dan' and row['geonames_country'] == 'Denmark'

        # SWEDISH
        swedish_language = row['language'] == 'swe' and row['geonames_country'] == 'Sweden'

        # NORWEGIAN
        norwegian_language = row['language'] == 'nor' and row['geonames_country'] == 'Norway'

        # FINNISH
        finnish_language = row['language'] == 'fin' and row['geonames_country'] == 'Finland'

        # ESTONIAN
        estonian_language = row['language'] == 'est' and row['geonames_country'] == 'Estonia'

        # LATVIAN
        latvian_language = row['language'] == 'lav' and row['geonames_country'] == 'Latvia'

        # LITHUANIAN
        lithuanian_language = row['language'] == 'lit' and row['geonames_country'] == 'Lithuania'

        # BULGARIAN
        bulgarian_language = row['language'] == 'bul' and row['geonames_country'] == 'Bulgaria'

        # MACEDONIAN
        macedonian_language = row['language'] == 'mac' and (serbo_croatian_speaking or row['geonames_country'] == 'North Macedonia')

        # GREEK
        greek_language = row['language'] == 'gre' and row['geonames_country'] == 'Greece'

        # UKRAINIAN
        ukrainian_language = row['language'] == 'ukr' and (row['geonames_country'] == 'Ukraine' or row['geonames_country'] == 'Russia')

        # BELARUSIAN
        belarusian_language = row['language'] == 'bel' and  (row['geonames_country'] == 'Belarus' or row['geonames_country'] == 'Russia')

        # TURKISH
        turkish_language = row['language'] == 'tur' and row['geonames_country'] == 'Turkey'

        # PORTUGUESE
        portuguese_language = row['language'] == 'por' and row['geonames_country'] == 'Portugal'

        # ALBANIAN
        albanian_language = row['language'] == 'alb' and row['geonames_country'] == 'Albania'

        # RUSSIAN
        russian_language = row['language'] == 'rus' and (row['geonames_country'] == 'Russia' or row['geonames_country'] == 'Belarus' or row['geonames_country'] == 'Ukraine' or 
                                                         row['geonames_country'] == 'Kazakhstan' or row['geonames_country'] == 'Moldova' or row['geonames_country'] == 'Uzbekistan')

        # SLOVAK
        slovak_language = row['language'] == 'slo' 

        # CATALAN
        catalan_speaking = row['region_country_name'] == 'Catalonia'
        catalan_language = row['language'] == 'cat'
        catalan_cond = catalan_language and catalan_speaking

        # ARABIC 
        arabic_language = row['language'] == 'ara'


        if plot_year < 1989:
            german_cond = german_language and (row['region_country_name'] == 'West Germany' or german_speaking) 
            german_countries = ['West Germany', 'Austria', 'Switzerland ger',  'Liechtenstein'] 

            german_east_cond = german_language and row['region_country_name'] == 'East Germany'

            germany_rest_cond = False

            # SOVIET
            #russian_speaking =  (row['geonames_country'] == 'Estonia' or row['geonames_country'] == 'Lithuania' or  row['geonames_country'] == 'Latvia' or  
            #                     row['geonames_country'] == 'Byelarus' or row['geonames_country'] == 'Ukraine' or row['geonames_country'] == 'Moldova' or
            #                     row['geonames_country'] == 'Russia' or row['geonames_country'] == 'Georgia' or row['geonames_country'] == 'Azerbaijan')
            
            russian_speaking = (row['geonames_country'] == 'Russia')
            soviet_cond = russian_language and russian_speaking
            #soviet_countries = ['Estonia', 'Lithuania', 'Latvia', 'Byelarus', 'Ukraine', 'Moldova', 'Russia', 'Georgia', 'Azerbaijan']
            soviet_countries = ['Russia']
            russian_cond = False

            slovak_speaking = row['geonames_country'] == 'Czechia' or row['geonames_country'] == 'Slovakia'
            slovak_cond = slovak_language and slovak_speaking


        else:
            german_cond = german_language and (row['geonames_country'] == 'Germany' or german_speaking)
            german_countries = ['West Germany', 'East Germany', 'Austria', 'Switzerland ger',  'Liechtenstein']

            german_east_cond = False 

            germany_rest_cond = row['geonames_country'] == 'Germany'
            soviet_cond = False   

            russia = row['geonames_country'] == 'Russia'
            russian_cond = russian_language and russia

            slovak_speaking = row['geonames_country'] == 'Slovakia'
            slovak_cond = slovak_language and slovak_speaking

            
        #### SLOVAK ###

        if slovak_cond:
            save_to_dict(['Slovakia'], plot_year, df_dict, row)  
            continue 

        
        ##### GERMAN SPEAKING ##### 

        if german_cond:
            save_to_dict(german_countries, plot_year, df_dict, row)  
            continue

        if german_east_cond:
            save_to_dict(['East Germany'], plot_year, df_dict, row)  
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

        #### CATALAN ####
        
        if catalan_cond:
            save_to_dict(['Catalonia'], plot_year, df_dict, row)  
            continue

        #### SOVIET ####

        if soviet_cond:
            save_to_dict(soviet_countries, plot_year, df_dict, row)    
            continue

        #### RUSSIA ####

        if russian_cond:
            save_to_dict(['Russia'], plot_year, df_dict, row)    
            continue

        #### ROMANIAN SPEAKING ####

        if romanian_cond:
            save_to_dict(romanian_countries, plot_year, df_dict, row)    
            continue

        #### SLOVENIAN ####

        if slovenian_language:
            save_to_dict(['Slovenia'], plot_year, df_dict, row)    
            continue

        #### POLAND ####

        if polish_language:
            save_to_dict(['Poland'], plot_year, df_dict, row)    
            continue

        #### DENMARK ####

        if danish_language:
            save_to_dict(['Denmark'], plot_year, df_dict, row)    
            continue

        #### SWEDEN ####

        if swedish_language:
            save_to_dict(['Sweden'], plot_year, df_dict, row)    
            continue

        #### NORWAY ####

        if norwegian_language:
            save_to_dict(['Norway'], plot_year, df_dict, row)    
            continue

        #### FINLAND ####

        if finnish_language:
            save_to_dict(['Finland'], plot_year, df_dict, row)    
            continue

        #### ESTONIA ####

        if estonian_language:
            save_to_dict(['Estonia'], plot_year, df_dict, row)    
            continue

        #### LATVIA ####

        if latvian_language:
            save_to_dict(['Latvia'], plot_year, df_dict, row)    
            continue

        #### LITHUANIA ####

        if lithuanian_language:
            save_to_dict(['Lithuania'], plot_year, df_dict, row)    
            continue

        #### BULGARIA ####

        if bulgarian_language:
            save_to_dict(['Bulgaria'], plot_year, df_dict, row)    
            continue
        
        #### NORTH MACEDONIA ####

        if macedonian_language:
            save_to_dict(['Macedonia'], plot_year, df_dict, row)    
            continue

        #### GREECE ####

        if greek_language:
            save_to_dict(['Greece'], plot_year, df_dict, row)    
            continue
            
        #### UKRAINE ####

        if ukrainian_language:
            save_to_dict(['Ukraine'], plot_year, df_dict, row)    
            continue    

        #### BELARUS ####

        if belarusian_language:
            save_to_dict(['Byelarus'], plot_year, df_dict, row)    
            continue 

        #### TURKEY ####

        if turkish_language:
            save_to_dict(['Turkey'], plot_year, df_dict, row)    
            continue 

        #### PORTUGAL ####

        if portuguese_language:
            save_to_dict(['Portugal'], plot_year, df_dict, row)    
            continue  

        #### ALBANIA ####

        if albanian_language:
            save_to_dict(['Albania'], plot_year, df_dict, row)    
            continue  

        #### ARABIC ####

        if arabic_language:
            save_to_dict(['Algeria', 'Tunisia', 'Syria'], plot_year, df_dict, row)     # 
            continue


#df = pd.DataFrame.from_dict(list(df_dict), columns=['country','map_year']).assign(weights=df_dict.values())

df = pd.Series(df_dict).reset_index()   
df.columns = ['country', 'map_year', 'weights'] 
#df['weights'] = df['weights'].apply(lambda x: math.log2(x))
df.to_csv('weights/weights_only_major_language_families_new.csv')            