import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import os
import re
import csv


def get_closest_lower_year(my_list, year):
    left, right = 0, len(my_list) - 1
    closest_lower = None

    while left <= right:
        mid = (left + right) // 2
        if my_list[mid] <= year:
            closest_lower = my_list[mid]
            left = mid + 1
        else:
            right = mid - 1

    return closest_lower


folder_path = "historical-basemaps/geojson"

# List all files in the folder
files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

print(files)

pattern = r'world_(\w{4})\.geojson'

# Get 4 digit year from the files
file_years = list(map(lambda x: re.search(pattern, x).group(1) if re.search(pattern, x) else None , files)) 
# Drop None
file_years = list(filter(lambda x: x is not None, file_years))
# Convert to integer
file_years = list(map(lambda x: int(x), file_years))

print(file_years)
geotagged_df = pd.read_csv("geotagged/geotagged_germany.csv")

saved_country_dict = {}

geotagged_df = geotagged_df.sort_values(by=['year'])

country_names = []
map_years = []

not_found_cities = {}
try:
    for i, geo_row in geotagged_df.iterrows():
        # Get year from the geotagged dataframe
        year = geo_row['year']

        # Find out the closest lower year 
        map_year = get_closest_lower_year(file_years, year)

        dict_key = (geo_row['geonames_name'], map_year)

        # 
        try:
            if saved_country_dict.get(dict_key) is None:
            
                # Path to geojson
                geojson_path = folder_path + '/world_' + str(map_year)+ '.geojson'

                # Load the basemap GeoJSON file into a GeoDataFrame
                historical_basemap = gpd.read_file(geojson_path)

                # Get coordinates from the geotagged df
                longitude = geo_row['geonames_lng']
                latitude = geo_row['geonames_lat']

                # Create a Point geometry object from the coordinates
                point = Point(longitude, latitude)

                found = False
                # Iterate over each country's geometry and check if the point is within it
                for index, row in historical_basemap.iterrows():
                    if row['geometry'].contains(point):
                        country_name = row['NAME']
                        print(f"{geo_row['geonames_name']} was in {str(year)} in {country_name}.")
                        saved_country_dict[dict_key] = country_name
                        found = True
                        break
            else:
                country_name =  saved_country_dict[dict_key]
                found = True
                
            map_years.append(map_year) 

            if found:    
                country_names.append(country_name)     
            else:
                k = (i, geo_row['geonames_name'], geo_row['year'])
                if geo_row['geonames_country'] in historical_basemap['NAME'].values:
                    country_names.append(geo_row['geonames_country'])
                    saved_country_dict[dict_key] = country_name
                    not_found_cities[k] = geo_row['geonames_country']
                else:
                    country_names.append(None) 
                    not_found_cities[k] = None               
        except:
            country_names.append(None)    
            map_years.append(None)      
except:
    print("error on row {i}")
finally:
    geotagged_df['map_year'] = map_years
    geotagged_df['historical_country_name'] = country_names
    geotagged_df.to_csv("geotagged_germany_historical_country.csv")

    flattened_data = [(key[0], key[1], key[2], value) for key, value in not_found_cities.items()]
    
    with open('cities_not_found.csv', 'w', newline='', encoding = 'utf8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Index', 'City', 'Year', 'Country'])
        # Write the data rows
        writer.writerows(flattened_data)


