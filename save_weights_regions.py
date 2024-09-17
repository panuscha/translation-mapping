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

countries_codes = pd.read_excel("geotagged/countries_codes.xlsx")
language_codes = pd.read_excel('geotagged/language_codes.xlsx')

# dictionary country:official language
df_countries_language = {country : (language_codes[language_codes['alpha2'] == language[0:2]]['alpha3-b'].squeeze() if language[0:2] in list(language_codes['alpha2']) else None) for country, language in zip(countries_codes['Country'], countries_codes['Languages']) }

# dictionary language: countries
df_language_countries = {language : [] for language in language_codes['alpha3-b']}
for c,l in df_countries_language.items(): 
    if l is not None:
        df_language_countries[l].append(c)

# German 
df_language_countries['ger'].append('West Germany') 
df_language_countries['ger'].append('East Germany') 
df_language_countries['ger'].append('Switzerland ger') 

# French 
df_language_countries['fre'].append('Canada fre')
df_language_countries['fre'].append('Switzerland fre')
df_language_countries['fre'].append('Belgium fre')
df_language_countries['fre'].append('Zaire')
df_language_countries['fre'].append('Congo')

# Dutch 
df_language_countries['dut'].append('Belgium dut')
df_language_countries['dut'].append('Netherlands')

# Catalan 
df_language_countries['cat'].append('Catalonia')

# Macedonia
df_language_countries['mac'].append('Macedonia')

#English
df_language_countries['eng'].append('Canada eng')
df_language_countries['eng'].append('South Africa') 
#df_language_countries['eng'].append('Cameroon') 

# Russian
df_language_countries['rus'].append('Kazakhstan') # MORE PEOPLE SPEAK RUSSIAN THAN KAZAKH
df_language_countries['rus'].append('Kyrgyzstan')
df_language_countries['bel'].append('Byelarus')

# Asia
df_language_countries['kor'].append('Korea, Republic of')
df_language_countries['kor'].append('Korea, Democratic People\'s Republic of')
df_language_countries['aze'].append('Azerbaijan')
df_language_countries['tgk'].append('Tajikistan')

# Africa
#df_language_countries['afr'].append('South Africa')

# Serbo-Croatia
df_language_countries['srp'].extend(['Bosnia and Herzegovina', 'Coatia', 'Serbia', 'Montenegro'])
df_language_countries['bos'].extend(['Bosnia and Herzegovina', 'Coatia', 'Serbia', 'Montenegro'])


# Europe or Other
region = 'Europe'

column_map_year = 'map_year_region' if region == 'Other' else 'map_year'

plot_years = [1945, 1956, 1967, 1978, 1989, 2000, 2011] 
#plot_years = geotagged_df[column_map_year].unique()
df_dict = {}

for plot_year in plot_years:     
    for _, row in geotagged_df[geotagged_df[column_map_year] == plot_year].iterrows():
        language = row['language']
        map_year = row[column_map_year]
        if language in df_language_countries.keys(): 
            save_to_dict(df_language_countries[language], map_year, df_dict, row)
        else:
            print(language)    
         
df = pd.Series(df_dict).reset_index()   
df.columns = ['country', 'map_year', 'weights'] 
#df['weights'] = df['weights'].apply(lambda x: math.log2(x))
df.to_csv('weights/weights_language_families_regions_11_years.csv')                     