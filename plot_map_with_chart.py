import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors
from itertools import compress


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


# Table with number of translations for each country, language and decade
df = pd.read_excel("weights\\translations_language_countries.xlsx")

# countries and languages from number_of_colors.py  
countries =["Italy", "Belgium", "United Kingdom", "Czechoslovakia", "Denmark", "Sweden", "Slovakia", "Spain", "Switzerland", "USSR", "Germany (Soviet)", "East Germany",  "Germany", "Yugoslavia", "Poland", "Austria", "Italy", "Hungary"]
languages = ["rus", "est", "arm", "glg", "ukr", "wen", "eng", "lit", "baq", "dut", "slv", "mac", "hrv", "epo", "hun", "ger", "cat", "fre", "slo", "other"]

except_countries = {"Czechoslovakia" : ["slo"], "Belgium" : ["fre", "dut"],  "Switzerland": ["ger", "fre"], "Yugoslavia": ["hrv"]}

# Palette for languages
my_color_palette = {}
all_colors =[plt.cm.tab20(i) for i in range(20)]

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]



for idx,y in enumerate(years):
    folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/years"

    # Load the GeoJSON map
    geojson_path = folder_path + '/world_' + str(y) + '.geojson' # str(y) - using 1930 map instead
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
    fig, ax = plt.subplots(figsize=(12, 8))

    gdf.clip(bbox).plot(facecolor=gdf.clip(bbox)['color'],edgecolor='black', linewidth=0.5,  ax=ax, legend=True) #

    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    fig.colorbar(cbar)

    # Iterate through countries to plot the bar chart                
    for country in countries: # 

        # Select only non empty rows that are in the decade and for that country
        if (not df[(df['map_year'] == int(y)) &  (df['country'] == country)].empty) and (country in gdf.clip(bbox).index ):

            # All non-empty rows
            h = df[(df['map_year'] == int(y)) &  (df['country'] == country)]
            
            # sort values by weights descending
            h = h.sort_values(by = 'weights', ascending = 0)
            
            # if only weights, change to h.weights
            sum_weights = sum(h.weights)
            
            
            
            # if major language is an exception
            if country in except_countries.keys():
                
                # find weight of that language or sum of languages
                h_max = sum(h[h['language'].isin(except_countries[country])].weights)
                
                # Discard major language
                h = h[~h['language'].isin(except_countries[country])]
            else:
                # major language
                h_max = max(h.weights)
            
                # Discard the most common language (= should be the major language)
                h = h.iloc[1:, :]
           
            # outher colors, major will always be transparent, major is displayed as black
            outer_colors = [my_color_palette['eng'] , 'black' ]

            # list of outer weights 
            weights_all = [h_max, sum_weights - h_max ]
            
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

            lat, lon = convert_coordinates(lat, lon, (1, 1))
            print("{country} centroid lat: {lat}, lon: {lon}".format(country = country, lat =  0.5*(1+lat/90), lon = 0.5*(1+lon/180)))
            ### THIS NEEDS TO BE FIXED! ### 
            ax_pie = fig.add_axes([ lat , lon , 0.05, 0.05], aspect='equal') #,[0.5*(1+lon/180) , 0.5*(1+lat/90)
            
            # outer pie
            n = ax_pie.pie(weights_all, radius=SIZE_OF_CHART, colors=outer_colors,center=(lon, lat),
            
            # white edges
            wedgeprops=dict(width=SIZE_OF_OUTER_CHART, edgecolor='w'))
            
            # set major language transparent
            n[0][0].set_alpha(0.0)

            # if there are minor languages translations
            if not(h.empty):
                
                # if there are more then TOP languages translations or any of the language is not in languages list
                if len(h.weights) > TOP or any(l not in languages for l in h.language):
                    
                    # sort values by weights descending
                    h = h.sort_values(by = 'weights', ascending = 0)
                    
                    # weights
                    weights_sorted = list(h.weights)
                    
                    h_lang = h.language.tolist()
                    
                    # index of languages that are in languages
                    ind_top_lang_trans = list(map(lambda i: True if h_lang[i] in languages else False ,range(len(h.language)) ))
                    
                    if sum(ind_top_lang_trans) > TOP:
                        res = [i for i, val in enumerate(ind_top_lang_trans) if val]
                        
                        #ind_under_top = ind_top_lang_trans[res[TOP]:]
                        
                        ind_top_lang_trans[res[TOP]:] = [False for i in range(len(ind_top_lang_trans) - res[TOP])]
                        #ind_top_lang_trans = ind_top_lang_trans[0:TOP]
                        # index of languages that are not in languages or under TOP threshold 
                        ind_not_top_trans = list(map(lambda i: True if h_lang[i] not in languages or i in res[TOP:] else False, range(len(h.language)) ))
                    else:
                        
                        # index of languages that are not in languages
                        ind_not_top_trans = list(map(lambda i: True if h_lang[i] not in languages else False, range(len(h.language)) ))
                    
                    
                    # "other" category languages
                    sum_not_top_lang = sum(list(compress(h.weights.tolist(), ind_not_top_trans))) #map(lambda i: weights_sorted[i], ind_not_top_trans)
                    df2_dict = {'country': country, 'language': "other", 'map_year': y, 'weights': sum_not_top_lang }
                    df2 = pd.DataFrame(data = df2_dict, index = ['0'])
                    
                    #idx = pd.Series(ind_top_lang_trans)
                    
                    # only non-other languages
                    h = h.iloc[ind_top_lang_trans, :]
                    
                    # combine two DataFrames
                    h = pd.concat([h, df2], ignore_index = True)
                    
                # get all colors for languages 
                inner_colors = [my_color_palette[l] for l in h.language  ]

                # get all languages 
                language = h.language
                
                # if only weights, change to h.weights
                weights = [w/sum_weights for w in h.weights] 


                # inner pie chart
                wedges, _ = ax_pie.pie(weights, radius=1-SIZE_OF_OUTER_CHART, colors=inner_colors,center=(lon, lat),
                wedgeprops=dict(edgecolor='w')) #width=size, 





    # Write years in the title 
    if y  == 1929:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(y), '1939'))
    elif idx < len(years)-1:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(y), str(int(years[idx+1])-1))) 
    else:
        ax.set_title('Europe Czech Translations {} - {}'.format(str(y), '2021'))
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    
    plt.savefig('plots/normalized with charts/'+ax.get_title() + '.png')
    #plt.show()
    