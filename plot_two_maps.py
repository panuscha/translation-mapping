import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from shapely.geometry import Polygon
import matplotlib.colors as colors

#geotagged_df = pd.read_excel("geotagged/geotagged_germany_country_update.xlsx")

#weights_df = pd.read_csv("weights/weights_language_families.csv")

#!!! Plots to language normalized major only folder !!!


#!!! Plots to current official language only folder !!!
#weights_df = pd.read_csv('weights/weights_only_major_language_families_new.csv')
#
language_geojson_path =  "historical-basemaps/temp/language_map_combined.geojson"#'language-basemaps/combined.geojson'

coast_geojson_path = "historical-basemaps/ne_50m_coastline"


regions_bbox =  {'Middle East'    : [  20,   4,  70,  44],
                 'North America'  : [-126, 7, -67, 60],#[-145, -10, -55,  62]
                 'Asia'           : [  70, -17, 160,  55], 
                 'Europe'         : [ -11, 36, 40, 64] } #[ -10,  35,  60,  75]


regions_bbox =  {'East'           : [29.1,   5, 143,  56],
                 'America'        : [-126,   1, -67,  55],
                 'Europe'         : [ -11,  36,  40,  64],
                 'World'          : [-130, -60, 165,  80]}
 

region_czech =  {'Middle East'    : 'Střední východ',
                 'North America'  : 'Severní a Střední Amerika',
                 'Asia'           : 'Asie', 
                 'Europe'         : 'Evropa'}

region_czech =  {'East'           : 'Východ',
                 'America'        : 'Amerika',
                 'World'          : 'Svět', 
                 'Europe'         : 'Evropa'}

region = 'Europe'#'World'   
write_title = True
combine_languages = True
if combine_languages:
    if region == 'Europe':
        plot_folder = "language normalized major only"
        weights_df = pd.read_csv('weights/weights_language_families.csv')
        title_middle = 'Překlady do hlavního a menšinového jazyka '
    else:
        print("This combination is available in plot_map.py only")
        sys.exit(0)    
 
else:
    if region == 'Europe':
        plot_folder = "current official language only Europe"
        title_middle = 'Překlady do hlavního jazyka'
        weights_df = pd.read_csv('weights/weights_only_major_language_families_new.csv')
    else:
        plot_folder = 'current official language only'   
        weights_df = pd.read_csv('weights/weights_language_families_regions_11_years.csv') 
        title_middle = 'Překlady do hlavního jazyka ve světě'

# Bounding box of the map 
bbox =  regions_bbox[region] 
#column_map_year = 'map_year'if region == 'Europe' else 'map_year_region'
column_map_year = 'map_year'

if region == 'Europe':
    map_years = list(map(lambda x: int(x),np.unique(weights_df['map_year'])))
else:    
    map_years = [1918, 1945, 1989]
    map_years = list(map(lambda x: int(x),np.unique(weights_df['map_year'])))



# Read basemap GeoJSON using GeoPandas
coloring_data = gpd.read_file(language_geojson_path)

coloring_data = coloring_data.clip(bbox)

# Normalize the data for the colormap
vmin = 1
vmax = 1
for year in weights_df[column_map_year].unique():
    for country in weights_df.loc[weights_df[column_map_year] == year, 'country' ].unique():
        if country in coloring_data['NAME'].tolist():
            vmax = max(vmax, weights_df.loc[(weights_df[column_map_year] == year) & (weights_df['country'] == country), 'weights'].sum())
print(vmax)

norm = colors.Normalize(vmin=vmin, vmax=vmax)


for idx, map_year in enumerate(map_years):
        
    weights_df_year = weights_df[weights_df[column_map_year] == map_year]

    # Load the GeoJSON map
    historical_geojson_path = 'historical-basemaps/temp/world_' + str(map_year)+ '.geojson' ### CHANGED TO TEMP FOLDER

    # Create a GeoDataFrame with a single polygon covering the world
    world_polygon = gpd.GeoDataFrame(geometry=[Polygon([(-180, -90), (180, -90), (180, 90), (-180, 90)])])

    # Read historical borders GeoJSON using GeoPandas
    historical_borders = gpd.read_file(historical_geojson_path).to_crs(epsg=4326)  

    # Read basemap GeoJSON using GeoPandas
    coloring_data = gpd.read_file(language_geojson_path).to_crs(epsg=4326)   

    # Merge weights with the basemap
    merged_coloring_data = coloring_data.merge(weights_df_year, left_on='NAME', right_on='country', how='left')

    merged_coloring_data = merged_coloring_data.set_index('NAME')
    
    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    #merged['color'] = '#ffffff' 
    merged_coloring_data['color'] = '#d3d3d3'

    # Set the color for countries with available data
    for _, row in weights_df[weights_df[column_map_year] == map_year].iterrows():
        country = row['country']
        weight = row['weights']
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            merged_coloring_data.loc[merged_coloring_data.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)

    height = 11
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1]
    aspect_ratio = bbox_width / bbox_height
    calculated_width = height* aspect_ratio

    # Create a base plot
    fig, ax = plt.subplots( figsize=(calculated_width, height))

    ax.set_xlim([bbox[0], bbox[2]])
    ax.set_ylim([bbox[1], bbox[3]])

    world_polygon.clip(bbox).plot(ax = ax, facecolor = 'lightblue', edgecolor='black')

    # Plot the choropleth map
    merged_coloring_data.clip(bbox).plot(ax = ax, facecolor=merged_coloring_data.clip(bbox)['color'], edgecolor='None', legend=True)

    #coloring_data.plot(ax=ax, color='red', edgecolor='none', linewidth=1)
    historical_borders.clip(bbox).plot(ax=ax, color='none', edgecolor='gray', linewidth=1.0)

    #coast_line.clip(bbox).plot(ax=ax,  color='white', linewidth=1)

    # Write years in title 
    if idx < len(map_years)-1:
        title_plot = '{} Czech Translations {} - {}'.format(region, str(map_year), str(int(map_years[idx+1])-1))
        title = '{} ({} - {})'.format(title_middle,  str(map_year), str(int(map_years[idx+1])-1)) #region_czech[region],
    else:
        title_plot = '{} Czech Translations {} - {}'.format(region, str(map_year), '2021') 
        #title_plot = '{} Czech Translations {}'.format(region, str(map_year)) 
        title = '{} ({} - {})'.format(title_middle,  str(map_year), '2021')# region_czech[region],
          
    plt.grid(False)
    ax.set_axis_off() 
    
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    # set colormap
    cb = fig.colorbar(cbar, ax = ax,shrink=0.865, pad = 0.01) #  
    # set label to colormap scale
    cb.set_label('Počet překladů za období', rotation=90)
    
    # plt.subplots_adjust(left=0,
    #                 bottom=0,
    #                 right=1,
    #                 top=1)
    
    if write_title:
        ax.set_title(title, fontsize=12)
        #fig.suptitle(title, fontsize=12)
        plt.savefig('plots/with title/{}/{}.svg'.format(plot_folder, title_plot))
    else:
        plt.savefig('plots/without title/{}/{}.svg'.format(plot_folder, title_plot))    

    # Show the plot
    #plt.show()
