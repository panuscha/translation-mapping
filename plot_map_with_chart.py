import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors
import os
import matplotlib.patches as mpatches

############ FOR MAPS #############

# folder with geopandas maps
folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/years"

 # Bounding box of the map - Europe
bbox =  [-10, 40, 40, 65] #[-10, 35, 60, 75] # [minx, miny, maxx, maxy] - minimal longitude, minimal latitude, maximal longitude, maximal latitude

# Path to the infos about translations  
geotagged_df = pd.read_excel("geotagged/geotagged_hist_country.xlsx")


# Dictionary with map years, historical names of countries and their weights 
plot_dict_dicts = {}

# iterate through rows 
for i, row in geotagged_df.iterrows():

    # if map year is present 
    if not math.isnan(row['map_year']):

        # map year 
        map_year = str(int(row['map_year']))

        # historical name of the country in that period 
        historic_name = row['historical_country_name']
        
        # weight
        weight = row['weight']

        # if the year is yet not in the dictionary
        if map_year not in plot_dict_dicts:

            # create a key where the map year is the key a value is a dictionary
            plot_dict_dicts[map_year] = {}

        # add a weight to a  combination of historical country and map year
        plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight

# all years of the map
years = ['1918', '1929', '1945', '1956', '1967', '1978', '1989', '2000', '2011']

# Normalize the data for the colormap
vmin = 1
vmax = 657.5 # from plot_two_maps
norm = colors.Normalize(vmin=vmin, vmax=vmax)

############# FOR CHARTS ################

# Radius of the charts
RADIUS = 1.1

# folder with charts
piechart_folder = 'plots\\pie charts minor top 19 languages plain\\'

# Table with number of translations for each country, language and decade
df = pd.read_excel("weights\\translations_language_countries.xlsx")

# countries and languages from number_of_colors.py  
countries =["Italy", "Belgium", "United Kingdom", "Czechoslovakia", "Denmark", "Sweden", "Slovakia", "Spain", "Switzerland", "USSR", "Germany (Soviet)", "East Germany",  "Germany", "Yugoslavia", "Poland", "Austria", "Italy", "Hungary"]
languages = ["rus", "est", "arm", "glg", "ukr", "wen", "eng", "lit", "baq", "dut", "slv", "mac", "hrv", "epo", "hun", "ger", "cat", "fre", "slo", "other"]

# Palette for languages
my_color_palette = {}
all_colors =[plt.cm.tab20(i) for i in range(20)]

# handles for legend
handles = []

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]
    handles.append(mpatches.Patch(color=all_colors[i], label=language))

### centroid of geometry
# Load the GeoJSON map
geojson_path = folder_path + '/world_' + str('2011') + '.geojson' # str(y) - using 1930 map instead
gdf = gpd.read_file(geojson_path)
country_geometry = gdf.clip(bbox)[gdf.clip(bbox).NAME == "Italy"]['geometry'].iloc[0]

# Compute the centroid of the country
centroid = country_geometry.centroid

# Get the latitude and longitude of the centroid
lat_Italy = centroid.y
lon_Italy = centroid.x


# iterate through the years of map
for idx,map_year in enumerate(years):

    # Load the GeoJSON map
    geojson_path = folder_path + '/world_' + str(map_year) + '.geojson' # str(y) - using 1930 map instead
    gdf = gpd.read_file(geojson_path)

    # Create a DataFrame from the dictionary
    data_df = pd.DataFrame(list(plot_dict_dicts[map_year].items()), columns=['country', 'weight'])
    data_df.set_index('country', inplace=True)
    
    # create a column 'weight' and set all values to 0
    gdf['weight'] = 0

    gdf = gdf.set_index('NAME')

    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    gdf['color'] = '#ffffff'

    # Set the color for countries with available data
    for country, weight in plot_dict_dicts[map_year].items():
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)

    # Plotting the choropleth map
    fig, ax = plt.subplots(figsize = (12,8))

    
    # Iterate through countries to plot the bar chart                
    for country in countries: # 
        
        # get the path to the image
        piechart_path = piechart_folder + '{country}_{year}.png'.format(country = country, year = map_year)

        # if chart exists
        if   os.path.isfile(piechart_path):  

            # load image
            image = plt.imread(piechart_path, format="png")

            # get geometry of the country
            country_geometry = gdf.clip(bbox)[gdf.clip(bbox).index == country]['geometry'].iloc[0]


            if int(map_year) < 1989 and country == 'Italy':
                
                lat = lat_Italy
                lon = lon_Italy
            else:
                # Compute the centroid of the country
                centroid = country_geometry.centroid

                # Get the latitude and longitude of the centroid
                lat = centroid.y
                lon = centroid.x

            # show image at the latitude and longitude of the plot
            im = ax.imshow(
                image,
                extent=(lon-2*RADIUS, lon+2*RADIUS, lat-RADIUS, lat+RADIUS),
                zorder=1 # show it in the front
                )
    # plot the map
    gdf.clip(bbox).plot(facecolor=gdf.clip(bbox)['color'],edgecolor='black', linewidth=0.5,  ax=ax, legend=True, zorder=0) #
    
    # colorbar 
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(cbar)
    plt.legend(handles=handles)        


    # Write years in the title 
    if map_year  == 1929:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(map_year), '1939'))
    elif idx < len(years)-1:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(map_year), str(int(years[idx+1])-1))) 
    else:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(map_year), '2021'))
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    
    plt.savefig('plots/normalized with charts/'+ax.get_title() + '.png')

    