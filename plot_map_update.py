import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors
from geopandas import GeoDataFrame
from shapely.geometry import Point
import numpy as np

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


def close_event():
    plt.close() #timer calls this function after 3 seconds and closes the window

geotagged_path = "geotagged_new_new.csv"
geotagged_df = pd.read_csv(geotagged_path)

plot_dict_dicts = {}

for i, row in geotagged_df.iterrows():
    if not math.isnan(row['year']):
        year = str(int(row['year']))
        historic_name = row['historical_coutry_name']
        weight = row['weight']
        if year not in plot_dict_dicts:
            plot_dict_dicts[year] = {}
        plot_dict_dicts[year][historic_name] = plot_dict_dicts[year].get(historic_name, 0) + weight

# Create a DataFrame from the dictionary
weights_df = pd.DataFrame(plot_dict_dicts).fillna(0)
#weights_df.to_csv('weights_df.csv')

# Transpose the DataFrame to have countries as rows and years as columns
weights_df = weights_df.T

# Optionally, you can rename the index column (years) to 'Year'
weights_df.index.name = 'Year'

window_size = 5
weights_df_ma = weights_df.rolling(window=window_size, axis=0, min_periods=1).mean()

#weights_df_ma.to_csv('weights_ma.csv')


file_years = list(filter(lambda x: not math.isnan(x) ,geotagged_df['map_year'].unique()))
file_years = list(map(lambda x: str(int(x)),file_years))

# years = list(filter(lambda x: not math.isnan(x) ,geotagged_df['year'].unique()))
# years = list(map(lambda x: str(int(x)),years))

years = list(map(lambda x: str(int(x)), list(range(1960,2021))))


# Normalize the data for the colormap
vmin = 1
vmax = weights_df_ma.to_numpy().max()
# for year in geotagged_df['year'].unique():
#     for hist_country in geotagged_df.loc[geotagged_df['year'] == year, 'historical_coutry_name' ].unique():
#         vmax = max(vmax, geotagged_df.loc[(geotagged_df['year'] == year) & (geotagged_df['historical_coutry_name'] == hist_country), 'weight'].sum())


norm = colors.Normalize(vmin=vmin, vmax=vmax)

for idx,y in enumerate(years):

    map_year = get_closest_lower_year(file_years, y)
    folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/geojson"

    # Load the GeoJSON map
    geojson_path = folder_path + '/world_' + str(map_year)+ '.geojson'
    gdf = gpd.read_file(geojson_path)
    gdf.set_index('NAME', inplace=True)

    common_countries_columns = weights_df_ma[weights_df_ma.index == y].columns.intersection(gdf.index).sort_values().dropna()

    # Create a DataFrame from the dictionary
    data_df = pd.DataFrame(list(plot_dict_dicts[y].items()), columns=['country', 'weight'])
    data_df.set_index('country', inplace=True)
    
    gdf['weight'] = 0

    # Set the weights for countries with available data
    for country in common_countries_columns:
        weight =  weights_df_ma[country][weights_df_ma.index == y ].T.sort_index().values
        # When the weight was below 1, it did not plot any colour 
        if weight > 0 :
            weight +=3
        if isinstance(gdf.loc[country, 'weight'], (int, float, np.int64, np.float64)):
            gdf.loc[country, 'weight'] = weight
        else:    
            gdf.loc[country, 'weight'] = [weight] * len(gdf.loc[country, 'weight'])
        #gdf.loc[common_countries_columns, 'weight'] = weights_df_ma[common_countries_columns.to_list()][weights_df_ma.index == y ].T.sort_index().values

    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    gdf['color'] = 'white'

    # Set the color for countries with available data
    # for country, weight in plot_dict_dicts[y].items():
    #     if weight > 0:
    #         color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
    #         gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)


    for country, row in gdf.iterrows() :
        if row['weight'] > 0:
            color_rgb = cmap(norm(row['weight']))[:3]  # Get RGB values from the colormap
            gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)




    geometry = [Point(xy) for xy in zip(geotagged_df.loc[geotagged_df['year'] == int(y),"geonames_lng"],geotagged_df.loc[geotagged_df['year'] == int(y),"geonames_lat"])]
    crs = {'init': 'epsg:4326'}
    caps_points = GeoDataFrame(geotagged_df.loc[geotagged_df['year'] == int(y),"geonames_name"], crs=crs, geometry=geometry)

    # Plotting the choropleth map
    fig, ax = plt.subplots(1, 1,  figsize=(15, 10) ) # 

    # Timer
    timer = fig.canvas.new_timer(interval = 3000) #creating a timer object and setting an interval of 3000 milliseconds
    timer.add_callback(close_event)

    ax.set_aspect('equal')  
    gdf.plot(facecolor=gdf['color'], edgecolor='0.8', linewidth=0.8, ax=ax, legend=True)
    #gdf.plot(column='weight', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    # Plot cities
    # caps_points.plot(ax = ax, marker = "p", markersize = 0.1, c = "red", )
    # Write years in title 
    ax.set_title('Choropleth Map {}'.format(str(y)))
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(cbar)
    plt.savefig('plots/individual years ma/'+ax.get_title() + '.png')
    #timer.start()
    #plt.show()
    close_event()
    