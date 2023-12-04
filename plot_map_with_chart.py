import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors
import os
import matplotlib.patches as mpatches


def getImage(path):
   return plt.imread(path, format="png")

# Function to convert latitude and longitude to x and y within a given figure size
def convert_coordinates(latitude, longitude, figure_size):
    lon_range = figure_size[0]  # Assuming longitude range corresponds to the figure width
    lat_range = figure_size[1]  # Assuming latitude range corresponds to the figure height

    x = (longitude - bbox[0]) / (bbox[2] - bbox[0]) * lon_range
    y = (latitude - bbox[1]) / (bbox[3] - bbox[1]) * lat_range

    return x, y


############ FOR MAPS #############

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

years = ['1918', '1929', '1945', '1956', '1967', '1978', '1989', '2000', '2011']

# Normalize the data for the colormap
vmin = 1
vmax = 657.5 # from plot_two_maps
norm = colors.Normalize(vmin=vmin, vmax=vmax)


############# FOR CHARTS ################

TOP = 3
MIN_TRANS = 4 
SIZE_OF_CHART = 0.2
# size of the outer chart
SIZE_OF_OUTER_CHART = 0.1 * SIZE_OF_CHART
RADIUS = 1.7


# Table with number of translations for each country, language and decade
df = pd.read_excel("weights\\translations_language_countries.xlsx")

# countries and languages from number_of_colors.py  
countries =["Italy", "Belgium", "United Kingdom", "Czechoslovakia", "Denmark", "Sweden", "Slovakia", "Spain", "Switzerland", "USSR", "Germany (Soviet)", "East Germany",  "Germany", "Yugoslavia", "Poland", "Austria", "Italy", "Hungary"]
languages = ["rus", "est", "arm", "glg", "ukr", "wen", "eng", "lit", "baq", "dut", "slv", "mac", "hrv", "epo", "hun", "ger", "cat", "fre", "slo", "other"]

except_countries = {"Czechoslovakia" : ["slo"], "Belgium" : ["fre", "dut"],  "Switzerland": ["ger", "fre"], "Yugoslavia": ["hrv"]}

# Palette for languages
my_color_palette = {}
all_colors =[plt.cm.tab20(i) for i in range(20)]
handles = []

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]
    handles.append(mpatches.Patch(color=all_colors[i], label=language))



for idx,plot_year in enumerate(years):
    folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/years"

    # Load the GeoJSON map
    geojson_path = folder_path + '/world_' + str(plot_year) + '.geojson' # str(y) - using 1930 map instead
    gdf = gpd.read_file(geojson_path)

    # Create a DataFrame from the dictionary
    data_df = pd.DataFrame(list(plot_dict_dicts[plot_year].items()), columns=['country', 'weight'])
    data_df.set_index('country', inplace=True)
    
    gdf['weight'] = 0

    gdf = gdf.set_index('NAME')

    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    gdf['color'] = '#ffffff'

    # Set the color for countries with available data
    for country, weight in plot_dict_dicts[plot_year].items():
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)


    # Bounding box of the map - Europe
    bbox =  [-10, 35, 60, 75] # [minx, miny, maxx, maxy] - minimal longitude, minimal latitude, maximal longitude, maximal latitude

    # Plotting the choropleth map
    fig, ax = plt.subplots(figsize = (12,8))

    
    # Iterate through countries to plot the bar chart                
    for country in countries: # 
        
        piechart_path = 'plots\\pie charts minor top 19 languages plain\\{country}_{year}.png'.format(country = country, year = plot_year)

        if   os.path.isfile(piechart_path):  

            # load image
            image = getImage(piechart_path)

            # # plot
            # fig, ax = plt.subplots()
            country_geometry = gdf.clip(bbox)[gdf.clip(bbox).index == country]['geometry'].iloc[0]

            # Compute the centroid of the country
            centroid = country_geometry.centroid

            # Get the latitude and longitude of the centroid
            lat = centroid.y
            lon = centroid.x
            #print("{country} centroid lat: {lat}, lon: {lon}".format(country = country, lat = lat, lon = lon))

            # Set the size of the pie chart within the map
            chart_size = 0.2  # Adjust this value as needed

            im = ax.imshow(
                image,
                extent=(lon-2*RADIUS, lon+2*RADIUS, lat-RADIUS, lat+RADIUS),
                zorder=1
                )

            #lat, lon = convert_coordinates(lat, lon, (1, 1))
            #lat =  math.cos(lat) * math.cos(lon)

    gdf.clip(bbox).plot(facecolor=gdf.clip(bbox)['color'],edgecolor='black', linewidth=0.5,  ax=ax, legend=True, zorder=0) #
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(cbar)
    plt.legend(handles=handles)        


    # Write years in the title 
    if plot_year  == 1929:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(plot_year), '1939'))
    elif idx < len(years)-1:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(plot_year), str(int(years[idx+1])-1))) 
    else:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(plot_year), '2021'))
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    
    plt.savefig('plots/normalized with charts/'+ax.get_title() + '.png')
    #plt.show()
    