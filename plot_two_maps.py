import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/"

#geotagged_df = pd.read_excel("geotagged/geotagged_germany_country_update.xlsx")
weights_df = pd.read_csv("weights/weights_language_families.csv")

map_years = np.unique(weights_df['map_year']) 

for idx, map_year in enumerate(map_years):
        
    weights_df_year = weights_df[weights_df['map_year'] == map_year]

    # Load the GeoJSON map
    historical_geojson_path = folder_path + 'historical-basemaps/geojson/world_' + str(map_year)+ '.geojson'

    # Read historical borders GeoJSON using GeoPandas
    historical_borders = gpd.read_file(historical_geojson_path)

    language_geojson_path = folder_path + 'language-basemaps/' + "combined.geojson"

    # Read basemap GeoJSON using GeoPandas
    coloring_data = gpd.read_file(language_geojson_path)

    # Merge weights with the basemap
    merged = coloring_data.merge(weights_df_year, left_on='NAME', right_on='country', how='left')

    # Bounding box of the map - Europe
    bbox =  [-10, 35, 60, 75] # [minx, miny, maxx, maxy] - minimal longitude, minimal latitude, maximal longitude, maximal latitude

    # Create a base plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Plot the choropleth map
    merged.clip(bbox).plot(ax = ax, column='weights', cmap='YlOrRd', edgecolor='None', legend=True)

    #coloring_data.plot(ax=ax, color='red', edgecolor='none', linewidth=1)
    historical_borders.clip(bbox).plot(ax=ax, color='none', edgecolor='black', linewidth=0.5)

    # Customize plot appearance
    if idx < len(map_years) - 1:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(map_year), map_years[idx+1]-1) )
    else:
        ax.set_title('Europe Czech Translations {}'.format(str(map_year)) )        
    plt.grid(False)
    ax.set_axis_off() 

    plt.savefig('plots/language/'+ax.get_title() + ' multiple.png')

    # Show the plot
    #plt.show()
