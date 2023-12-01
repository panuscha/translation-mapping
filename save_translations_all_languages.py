import pandas as pd
import math

def save_to_dict(map_year, df_dict, row):
    lang = row['language']
    if lang == 'srp' or lang == 'bos' :
        lang = 'hrv'
    country = row['historical_country_name']
    key = (country, lang, map_year) 
    if key in df_dict:
        df_dict[key] += row['weight']   
    else:
        df_dict[key] =  row['weight']

#geotagged_df = pd.read_csv("geotagged/geotagged_germany_country_update.csv")
geotagged_df = pd.read_excel("geotagged/geotagged_hist_country.xlsx")


plot_years = ['1918', '1929', '1945', '1956', '1967', '1978', '1989', '2000', '2011']
df_dict = {}

for plot_year in plot_years:     
    for _, row in geotagged_df[geotagged_df['map_year'] == int(plot_year)].iterrows():
          
        save_to_dict(plot_year, df_dict, row)
        
 

df = pd.Series(df_dict).reset_index()   
df.columns = ['country', 'language', 'map_year', 'weights'] 
#df['weights'] = df['weights'].apply(lambda x: math.log2(x))
df.to_excel('weights/translations_language_countries.xlsx')            