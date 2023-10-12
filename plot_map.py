import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors

geotagged_df = pd.read_excel("geotagged/geotagged_hist_country.xlsx")

plot_dict_dicts = {}

for i, row in geotagged_df.iterrows():
    if not math.isnan(row['map_year']):
        map_year = str(int(row['map_year']))
        historic_name = row['historical_country_name']
        weight = row['weight']
        if map_year not in plot_dict_dicts:
            plot_dict_dicts[map_year] = {}
        plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight

#years = list(filter(lambda x: not math.isnan(x) ,geotagged_df['map_year'].unique()))
#years = list(map(lambda x: str(int(x)),years))
years = ['1920', '1930']

# Normalize the data for the colormap
vmin = 1
vmax = 657.5 # from plot_two_maps
norm = colors.Normalize(vmin=vmin, vmax=vmax)

for idx,y in enumerate(years):
    folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/geojson"

    # Load the GeoJSON map
    geojson_path = folder_path + '/world_' + str(1930) + '.geojson' # str(y) - using 1930 map instead
    gdf = gpd.read_file(geojson_path)

    # Create a DataFrame from the dictionary
    data_df = pd.DataFrame(list(plot_dict_dicts[y].items()), columns=['country', 'weight'])
    data_df.set_index('country', inplace=True)
    
    gdf['weight'] = 0

    gdf = gdf.set_index('NAME')

    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    gdf['color'] = '#ffffff'

    # Set the color for countries with available data
    for country, weight in plot_dict_dicts[y].items():
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)


    # Bounding box of the map - Europe
    bbox =  [-10, 35, 60, 75] # [minx, miny, maxx, maxy] - minimal longitude, minimal latitude, maximal longitude, maximal latitude

    # Plotting the choropleth map
    fig, ax = plt.subplots(1, 1,  figsize=(15, 10))

    gdf.clip(bbox).plot(facecolor=gdf.clip(bbox)['color'],edgecolor='black', linewidth=0.5,  ax=ax, legend=True) #

    # Write years in title 
    if idx < len(years)-1:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(y), str(int(years[idx+1])-1)))
    else:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(y), '1939'))
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(cbar)

    plt.savefig('plots/'+ax.get_title() + '.png')
    plt.show()
    