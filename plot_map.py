import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors

geotagged_df = pd.read_excel("geotagged/geotagged_hist_country.xlsx")
geotagged_df['geonames_lng'] = geotagged_df['geonames_lng'].apply(lambda x: float(str(x)) if isinstance(x, str) else -1000)
geotagged_df['geonames_lat'] = geotagged_df['geonames_lat'].apply(lambda x: float(str(x)) if isinstance(x, str) else -1000)
geotagged_df['map_year'] = geotagged_df['map_year'].apply(lambda x: str(int(x)))

plot_dict_dicts = {}

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

regions_bbox =  {'Middle East'    : [  25,   4,  70,  40],
                 'North America'  : [-145, -10, -55,  62],
                 'Asia'           : [  70, -10, 160,  62], 
                 'Europe'         : [ -10,  35,  60,  75] } 

region = 'Asia'

# Bounding box of the map 
bbox =  regions_bbox[region] 

for i, row in geotagged_df.iterrows():
    if not pd.isnull(row['map_year']):
        map_year = row['map_year']
        historic_name = row['historical_country_name']
        weight = row['weight']
        if map_year not in plot_dict_dicts:
            plot_dict_dicts[map_year] = {}
        plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight

#years = list(filter(lambda x: not math.isnan(x) ,geotagged_df['map_year'].unique()))
#years = list(map(lambda x: str(int(x)),years))
years = ['1918', '1945', '1989']

# Find cities that falls within the bbox of region 
bbox_lon = (geotagged_df['geonames_lng'] >= bbox[0]) & (geotagged_df['geonames_lng'] <= bbox[2])
bbox_lat = (geotagged_df['geonames_lat'] >= bbox[1]) & (geotagged_df['geonames_lat'] <= bbox[3])
gdf_clip = geotagged_df[bbox_lon & bbox_lat]


# Normalize the data for the colormap
vmin = 1
vmax = 1
year_countries = {year: [] for year in years}

for year in years:
    for hist_country in gdf_clip.loc[gdf_clip['map_year'] == year, 'historical_country_name' ].unique():
        vmax = max(vmax, gdf_clip.loc[(gdf_clip['map_year'] == year) & (gdf_clip['historical_country_name'] == hist_country), 'weight'].sum())
        year_countries[year].append(hist_country)
print(vmax)

norm = colors.Normalize(vmin=vmin, vmax=vmax)

for idx,y in enumerate(years):
    folder_path = "historical-basemaps/years"

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


   
    # Plotting the choropleth map
    fig, ax = plt.subplots(1, 1,  figsize=(12, 8))

    gdf.clip(bbox).plot(facecolor=gdf.clip(bbox)['color'],edgecolor='black', linewidth=0.5,  ax=ax, legend=True) #

    # Write years in title 
    if idx < len(years)-1:
        title = '{} Czech Translations {} - {}'.format(region, str(y), str(int(years[idx+1])-1))
    else:
        title = '{} Czech Translations {} - {}'.format(region, str(y), '2019')
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    
    # cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    # fig.colorbar(cbar)

    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    # set colormap
    cb = fig.colorbar(cbar, ax = ax, shrink=0.9)
    
    # set label to colormap scale
    cb.set_label('Počet překladů za období v dané zemi', rotation=90)
    
    plt.subplots_adjust(left=0,
                    bottom=0,
                    right=1,
                    top=1)

    plt.savefig('plots/normalized/'+title + '.png')

    # Print the countries that were not found in gdf 
    p = [country if country not in gdf.index else None for country in year_countries[y]]
    print("year",  y)
    print(p)
    #plt.show()
    