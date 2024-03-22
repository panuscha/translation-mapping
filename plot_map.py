import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from shapely.geometry import Polygon
from collections import defaultdict 
import pickle

def countries_into_languages(df):
    languages_countries = defaultdict(list)
    for _, row in df.iterrows():
        if isinstance(row['Official_language'], str):
            languages = list(row['Official_language'].split(","))
            for language in languages:
                languages_countries[language].append(row['Country'])
    return languages_countries                

geotagged_df = pd.read_excel("geotagged/geotagged_hist_country.xlsx")
geotagged_df['geonames_lng'] = geotagged_df['geonames_lng'].apply(lambda x: float(str(x)) if isinstance(x, str) else -1000)
geotagged_df['geonames_lat'] = geotagged_df['geonames_lat'].apply(lambda x: float(str(x)) if isinstance(x, str) else -1000)

column_map_year = 'map_year'
geotagged_df[column_map_year] = geotagged_df[column_map_year].apply(lambda x: str(int(x)))

plot_dict_dicts = {}

countries_info = pd.read_excel("geotagged/countries_info_new.xlsx")
languages_countries = countries_into_languages(countries_info)


# [minx, miny, maxx, maxy] - minimal longitude, minimal latitude, maximal longitude, maximal latitude

# pomocne vypocty xdddd
me_lon = 60
me_lat = 36

am_lon = 90
am_lat = 72

a_lon = 90
a_lat = 72

e_lon = 50
e_lat = 40

regions_bbox =  {'Middle East'    : [  20,   4,  70,  44],
                 'North America'  : [-145, -10, -55,  62],
                 'Asia'           : [  70, -17, 160,  55], 
                 'Europe'         : [ -10,  35,  60,  75], 
                'World'           : [-130, -60, 165,  80] } 

region_czech = {'Middle East'     : 'Střední východ',
                 'North America'  : 'Severní Amerika',
                 'Asia'           : 'Asie', 
                 'Europe'         : 'Evropa', 
                 'World'          : 'Svět'}

title_middle = 'Potenciál dosahu překladů ve světě'


region = 'World' 
write_title = True  

# Bounding box of the map 
bbox =  regions_bbox[region] 
years = ['1945', '1956', '1967', '1978', '1989', '2000', '2011'] 

# for i, row in geotagged_df.iterrows():
#     if not pd.isnull(row[column_map_year]) and row[column_map_year] in years:
#         map_year = row[column_map_year]
#         historic_name = row['historical_country_name']
#         weight = row['weight']
#         language = row['language']
#         if map_year not in plot_dict_dicts:
#             plot_dict_dicts[map_year] = {}
#         plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight
#         for country in languages_countries[language]:
#             historical_country_name = geotagged_df[(geotagged_df['geonames_country'] == country) & (geotagged_df[column_map_year] == map_year)]['historical_country_name']
#             if not historical_country_name.empty:
#                 historic_name = historical_country_name.iloc[0]
#                 plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight
#             else:
#                 plot_dict_dicts[map_year][country] = plot_dict_dicts[map_year].get(country, 0) + weight    

with open('weights/weights_potetial.obj', 'rb') as f:
    plot_dict_dicts = pickle.load(f)


#years = list(filter(lambda x: not math.isnan(x) ,geotagged_df['map_year'].unique()))
#years = list(map(lambda x: str(int(x)),years))
#years = ['1918', '1945', '1989']


# Find cities that falls within the bbox of region 
bbox_lon = (geotagged_df['geonames_lng'] >= bbox[0]) & (geotagged_df['geonames_lng'] <= bbox[2])
bbox_lat = (geotagged_df['geonames_lat'] >= bbox[1]) & (geotagged_df['geonames_lat'] <= bbox[3])
gdf_clip = geotagged_df[bbox_lon & bbox_lat]


# Normalize the data for the colormap
vmin = 1
vmax = 1
year_countries = {year: [] for year in years}

for year in years:
    for hist_country in gdf_clip.loc[gdf_clip[column_map_year] == year, 'historical_country_name' ].unique():
        vmax = max(vmax, gdf_clip.loc[(gdf_clip[column_map_year] == year) & (gdf_clip['historical_country_name'] == hist_country), 'weight'].sum())
        print(str(hist_country) + ' ' + str(year) + ' : ' + str(vmax))
        year_countries[year].append(hist_country)
print(vmax)

norm = colors.Normalize(vmin=vmin, vmax=vmax)

for idx,y in enumerate(years):
    folder_path = "historical-basemaps/years"

    # Create a GeoDataFrame with a single polygon covering the world
    world_polygon = gpd.GeoDataFrame(geometry=[Polygon([(-180, -90), (180, -90), (180, 90), (-180, 90)])])

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
    #gdf['color'] = '#ffffff' 
    gdf['color'] = '#d3d3d3'
    # Set the color for countries with available data
    for country, weight in plot_dict_dicts[y].items():
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)


   
    height = 11
    bbox_width = bbox[2] - bbox[0]
    bbox_height = bbox[3] - bbox[1]
    aspect_ratio = bbox_width / bbox_height
    calculated_width = height* aspect_ratio

    # Create a base plot
    fig, ax = plt.subplots( figsize=(calculated_width, height))

    world_polygon.clip(bbox).plot(ax = ax, facecolor = 'lightblue', edgecolor='black')

    gdf.clip(bbox).plot(facecolor=gdf.clip(bbox)['color'], edgecolor='gray', linewidth=1.0,  ax=ax, legend=True) #

    # Write years in title 
    if idx < len(years)-1:
        title_plot = '{} Czech Translations {} - {}'.format(region, str(y), str(int(years[idx+1])-1))
        title = '{} ({} - {})'.format(title_middle, str(int(years[idx])), str(int(years[idx+1])-1))
    else:
        title_plot = '{} Czech Translations {} - {}'.format(region, str(y), '2021')
        title = '{} ({} - {})'.format(title_middle, str(int(years[idx])), '2021')
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    
    # cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    # fig.colorbar(cbar)

    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    # set colormap
    cb = fig.colorbar(cbar, ax = ax, shrink=0.865, pad = 0.01)

    ax.set_xlim([bbox[0], bbox[2]])
    ax.set_ylim([bbox[1], bbox[3]])
    
    # set label to colormap scale
    cb.set_label('Počet překladů za období', rotation=90)
    
    if write_title:
        ax.set_title(title, fontsize=12)
        plt.savefig('plots/with title/potential/'+title_plot + '.svg')
    else:    
        plt.savefig('plots/without title/potential/'+title_plot + '.svg')

    # Print the countries that were not found in gdf 
    p = [country if country not in gdf.index else None for country in year_countries[y]]
    print("year",  y)
    print(p)
    #plt.show()
    