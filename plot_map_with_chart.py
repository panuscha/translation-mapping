import geopandas as gpd
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors
import os
import matplotlib.patches as mpatches
import svglib
from io import BytesIO
from shapely.geometry import Polygon
import shutil


matplotlib.rcParams['svg.fonttype'] = 'none'

############ FOR MAPS #############

# folder with geopandas maps
folder_path = "historical-basemaps/temp"

 # Bounding box of the map - Europe
bbox = [ -11,  36,  40,  64]# [-10, 40, 40, 65] #[-10, 35, 60, 75] # [minx, miny, maxx, maxy] - minimal longitude, minimal latitude, maximal longitude, maximal latitude

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

        # plot Czech republic gray 
        if historic_name != 'Czech Republic':

            # if the year is yet not in the dictionary
            if map_year not in plot_dict_dicts:

                # create a key where the map year is the key a value is a dictionary
                plot_dict_dicts[map_year] = {}

            # add a weight to a  combination of historical country and map year
            plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight

with_title = True

# Table with number of translations for each country, language and decade
df = pd.read_excel("weights/translations_language_countries.xlsx")

# all years of the map
years = ['1918', '1929', '1945', '1956', '1967', '1978', '1989', '2000', '2011']
column_map_year = 'map_year'

# Normalize the data for the colormap
vmin = 1

vmax = 1
for year in df[column_map_year].unique():
    for country in df.loc[df[column_map_year] == year, 'country' ].unique():
        vmax = max(vmax, df.loc[(df[column_map_year] == year) & (df['country'] == country), 'weights'].sum())
#vmax = 657.5 # from plot_two_maps - TODO: Change this number 
norm = colors.Normalize(vmin=vmin, vmax=vmax)

############# FOR CHARTS ################

# Radius of the charts
RADIUS = 1.1

# folder with charts
piechart_folder = 'plots/without title/pie charts minor top 19 languages plain new/'



# countries and languages from number_of_colors.py  
#countries =["Italy", "Belgium", "United Kingdom", "Czechoslovakia", "Denmark", "Sweden", "Slovakia", "Spain", "Switzerland", "USSR", "Germany (Soviet)", "East Germany",  "Germany", "Yugoslavia", "Poland", "Austria", "Italy", "Hungary"]
countries = df.country.unique()
#languages = ["rus", "est", "arm", "glg", "ukr", "wen", "eng", "lit", "baq", "dut", "slv", "mac", "hrv", "epo", "hun", "ger", "cat", "fre", "slo", "other"]
languages = {"rus": "ruština",
                   "est": "estonština",
                   "arm": "arménština",
                   "glg": "galicijština", 
                   "ukr": "ukrajinština",
                   "wen": "lužická srbština",
                   "eng": "angličtina",
                   "lit": "litevština",
                   "baq": "baskičtina",
                   "dut": "nizozemština",
                   "slv": "slovinština",
                   "mac": "makedonština",
                   "hrv": "srbochorvatština",
                   "epo": "esperanto",
                   "hun": "maďarština",
                   "ger": "němčina",
                   "cat": "katalánština",
                   "fre": "francouzština",
                   "slo": "slovenština",
                   "other": "ostatní jazyky"}

# Palette for languages
my_color_palette = {}
all_colors =[plt.cm.tab20(i) for i in range(20)]

# handles for legend
handles = []

# Save color for each country
for i, (language_code, language_czech) in enumerate(languages.items()):
    my_color_palette[language_code] = all_colors[i]
    handles.append(mpatches.Patch(color=all_colors[i], label=language_czech))

### centroid of geometry
# Load the GeoJSON map
geojson_path = folder_path + '/world_' + str('2011') + '.geojson' # str(y) - using 1930 map instead
gdf = gpd.read_file(geojson_path)


country_geometry = gdf.clip(bbox)[gdf.clip(bbox).NAME == "Italy"]['geometry'].iloc[0]

# Compute the centroid of the country
centroid = country_geometry.centroid

# Get the latitude and longitude of the centroid
lat_Italy = centroid.y
lon_Italy = centroid.x + 0.3


# iterate through the years of map
for idx,map_year in enumerate(years):

    # Load the GeoJSON map
    geojson_path = folder_path + '/world_' + str(map_year) + '.geojson' # str(y) - using 1930 map instead
    gdf = gpd.read_file(geojson_path) 

    gdf = gdf.dropna(subset=['NAME'])
    
    
    height = 11
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1]
    aspect_ratio = bbox_width / bbox_height
    calculated_width = height* aspect_ratio

    # Create a base plot
    fig, ax = plt.subplots( figsize=(calculated_width, height))

    ax.set_xlim([bbox[0], bbox[2]])
    ax.set_ylim([bbox[1], bbox[3]])

    

    
    
    # Create a GeoDataFrame with a single polygon covering the world
    world_polygon = gpd.GeoDataFrame(geometry=[Polygon([(-180, -90), (180, -90), (180, 90), (-180, 90)])])

    # Create a DataFrame from the dictionary
    data_df = pd.DataFrame(list(plot_dict_dicts[map_year].items()), columns=['country', 'weight'])
    data_df.set_index('country', inplace=True)
    
    # create a column 'weight' and set all values to 0
    gdf['weight'] = 0

    gdf = gdf.set_index('NAME')

    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    gdf['color'] =  '#d3d3d3'#'#ffffff'

    # Set the color for countries with available data
    for country, weight in plot_dict_dicts[map_year].items():
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)
        #else: gdf.loc[gdf.index == country, 'color'] = '#d3d3d3'

   

    
    # Iterate through countries to plot the bar chart                
    for country in countries: # 
        
        # get the path to the image
        piechart_path = piechart_folder + '{country}_{year}.svg'.format(country = country, year = map_year)


        # if chart exists
        if   os.path.isfile(piechart_path) and country in gdf.clip(bbox).index:  

            # Define the destination folder (the folder where you want to move the file)
            destination_folder = f'plots/without title/svg pie charts/{map_year}/' 

            # Create the full path for the destination
            destination_file = os.path.join(destination_folder, os.path.basename(piechart_path))

            # Ensure the destination folder exists, create it if it doesn't
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            # Move the file
            shutil.copy(piechart_path, destination_file)

            ### PLOT MAP WITHOUT CHART

            # # load image
            #image = plt.imread(piechart_path, format="png")
            

            # # Use Matplotlib to display the PNG image
            # #image = plt.imread(BytesIO(png_image))

            # # get geometry of the country
            # country_geometry = gdf.clip(bbox)[gdf.clip(bbox).index == country]['geometry'].iloc[0]


            # if  country == 'Italy': #int(map_year) < 1989 and
                
            #     lat = lat_Italy
            #     lon = lon_Italy 

            # elif int(map_year) < 1989 and country == 'West Germany':
                
            #     # Compute the centroid of the country
            #     centroid = country_geometry.centroid
                
            #     lat = centroid.y - 1
            #     lon = centroid.x   

            # elif country == 'United Kingdom': 

            #     # Compute the centroid of the country
            #     centroid = country_geometry.centroid

            #     lat = centroid.y - 1
            #     lon = centroid.x + 1      
            
            # else:
            #     # Compute the centroid of the country
            #     centroid = country_geometry.centroid

            #     # Get the latitude and longitude of the centroid
            #     lat = centroid.y
            #     lon = centroid.x 

            # # show image at the latitude and longitude of the plot
            # im = ax.imshow(
            #     image,
            #     extent=(lon-1.9*RADIUS, lon+1.9*RADIUS, lat-RADIUS, lat+RADIUS),
            #     zorder=1 # show it in the front
            #     )
            
    world_polygon.clip(bbox).plot(ax = ax, facecolor = 'lightblue', edgecolor='black', zorder=0 )
    gdf.clip(bbox).plot(ax=ax, facecolor=gdf.clip(bbox)['color'],edgecolor='gray', linewidth=1.0,  legend=True, zorder=0) #
    
    # plot the map
    
    
    # colorbar 
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    # set colormap
    cb = fig.colorbar(cbar, ax = ax, pad = 0.01) #shrink=0.9
    # set label to colormap scale
    cb.set_label('Počet překladů za období', rotation=90)
    
    # add legend 
    plt.legend(handles=handles, loc = "lower right", fontsize = "small", bbox_to_anchor=(1, 0)) #(0.961, 0.039)       




    # Write years in the title 
    if map_year  == str(1929):
        title_plot = 'Europe Czech Translations {} - {}'.format(str(map_year), '1939')
        title = 'Překlady do hlavního jazyka a ostatních jazyků (Evropa {} - {})'.format(str(map_year), '1939')
    elif idx < len(years)-1:
        title_plot = 'Europe Czech Translations {} - {}'.format(str(map_year), str(int(years[idx+1])-1))
        title = 'Překlady do hlavního jazyka a ostatních jazyků (Evropa {} - {})'.format(str(map_year), str(int(years[idx+1])-1))
    else:
        title_plot  = 'Europe Czech Translations {}'.format(str(map_year))
        title = 'Překlady do hlavního jazyka a ostatních jazyků (Evropa {} - {})'.format(str(map_year), '2019')
    ax.set_axis_off()  # Turn off the axis to remove the axis frame

    # plt.subplots_adjust(left=0,
    #                 bottom=0,
    #                 right=1,
    #                 top=1)
    if with_title:
        ax.set_title(title, fontsize=12)
        plt.savefig('plots/with title/maps without charts/'+title_plot + '.svg')
        #plt.savefig('plots/with title/normalized with charts new/'+title_plot + '.svg')
    else: 
        #plt.savefig('plots/without title/normalized with charts new/'+title_plot + '.svg')    
        plt.savefig('plots/without title/maps without charts/'+title_plot + '.svg')
    