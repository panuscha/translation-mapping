import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from shapely.geometry import Polygon
from collections import defaultdict 
import pickle 

def countries_into_languages(df):
    languages_countries = defaultdict(list)
    for _, row in df.iterrows():
        if isinstance(row['Official_language'], str):
            languages = list(row['Official_language'].split(","))
            for language in languages:
                languages_countries[language].append(row['Country'])
    return languages_countries                

geotagged_df = pd.read_excel("geotagged/geotagged_hist_country.xlsx")

column_map_year = 'map_year'
geotagged_df[column_map_year] = geotagged_df[column_map_year].apply(lambda x: str(int(x)))

plot_dict_dicts = {}

countries_info = pd.read_excel("geotagged/countries_info_new.xlsx")
languages_countries = countries_into_languages(countries_info)

years = ['1945', '1956', '1967', '1978', '1989', '2000', '2011'] 

for i, row in geotagged_df.iterrows():
    if not pd.isnull(row[column_map_year]) and row[column_map_year] in years:
        map_year = row[column_map_year]
        historic_name = row['historical_country_name']
        weight = row['weight']
        language = row['language']
        if map_year not in plot_dict_dicts:
            plot_dict_dicts[map_year] = {}
        plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight
        for country in languages_countries[language]:
            # historical_country_name = geotagged_df[(geotagged_df['geonames_country'] == country) & (geotagged_df[column_map_year] == map_year)]['historical_country_name']
            # if not historical_country_name.empty:
            #     historic_names = historical_country_name.unique()
            #     for historic_name in historic_names:
            #         plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight
            # else:
                if country != historic_name:
                    plot_dict_dicts[map_year][country] = plot_dict_dicts[map_year].get(country, 0) + weight 

   


with open('weights/weights_potential.obj', 'wb') as f:
    pickle.dump(plot_dict_dicts, f,  protocol=pickle.HIGHEST_PROTOCOL)

# Use dumps() to make it serialized 
serialized = pickle.dumps(plot_dict_dicts) 
  