import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import matplotlib.colors as colors

#geotagged_df = pd.read_excel("geotagged/geotagged_germany_country_update.xlsx")
#weights_df = pd.read_csv("weights/weights_language_families.csv")
weights_df = pd.read_csv('weights/weights_only_major_language_families.csv')

map_years = np.unique(weights_df['map_year']) 

# Normalize the data for the colormap
vmin = 1
vmax = 1
for year in weights_df['map_year'].unique():
    for hist_country in weights_df.loc[weights_df['map_year'] == year, 'country' ].unique():
        vmax = max(vmax, weights_df.loc[(weights_df['map_year'] == year) & (weights_df['country'] == hist_country), 'weights'].sum())
print(vmax)

norm = colors.Normalize(vmin=vmin, vmax=vmax)


for idx, map_year in enumerate(map_years):
        
    weights_df_year = weights_df[weights_df['map_year'] == map_year]

    # Load the GeoJSON map
    #historical_geojson_path = folder_path + 'historical-basemaps/geojson/world_' + str(map_year)+ '.geojson'
    historical_geojson_path = 'historical-basemaps/years/world_' + str(map_year)+ '.geojson'

    # Read historical borders GeoJSON using GeoPandas
    historical_borders = gpd.read_file(historical_geojson_path)

    language_geojson_path = 'language-basemaps/' + "combined.geojson"

    # Read basemap GeoJSON using GeoPandas
    coloring_data = gpd.read_file(language_geojson_path)

    # Merge weights with the basemap
    merged = coloring_data.merge(weights_df_year, left_on='NAME', right_on='country', how='left')

    merged = merged.set_index('NAME')
    
    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    merged['color'] = '#ffffff'

    # Set the color for countries with available data
    for _, row in weights_df[weights_df['map_year'] == map_year].iterrows():
        country = row['country']
        weight = row['weights']
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            merged.loc[merged.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)

    # Bounding box of the map - Europe
    bbox = [-10, 40, 40, 65] # [minx, miny, maxx, maxy] - minimal longitude, minimal latitude, maximal longitude, maximal latitude

    # Create a base plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Plot the choropleth map
    merged.clip(bbox).plot(ax = ax, facecolor=merged.clip(bbox)['color'], edgecolor='None', legend=True)

    #coloring_data.plot(ax=ax, color='red', edgecolor='none', linewidth=1)
    historical_borders.clip(bbox).plot(ax=ax, color='none', edgecolor='black', linewidth=0.5)

    # Customize plot appearance
    if idx < len(map_years) - 1:
        title = 'Europe Czech Translations {} - {}'.format(str(map_year), map_years[idx+1]-1)
    else:
        title ='Europe Czech Translations {}'.format(str(map_year))      
    plt.grid(False)
    ax.set_axis_off() 

    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    # set colormap
    cb = fig.colorbar(cbar, ax = ax, shrink=0.9)
    
    # set label to colormap scale
    cb.set_label('Počet překladů za období v dané zemi', rotation=90)

    plt.savefig('plots/language normalized major only/'+title + '.svg')

    # Show the plot
    #plt.show()
