import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.colors as colors

def close_event():
    plt.close() #timer calls this function after 3 seconds and closes the window

geotagged_df = pd.read_csv("geotagged_new.csv")

plot_dict_dicts = {}

for i, row in geotagged_df.iterrows():
    if not math.isnan(row['map_year']):
        map_year = str(int(row['map_year']))
        historic_name = row['historical_coutry_name']
        weight = row['weight']
        if map_year not in plot_dict_dicts:
            plot_dict_dicts[map_year] = {}
        plot_dict_dicts[map_year][historic_name] = plot_dict_dicts[map_year].get(historic_name, 0) + weight

years = list(filter(lambda x: not math.isnan(x) ,geotagged_df['map_year'].unique()))
years = list(map(lambda x: str(int(x)),years))

# Normalize the data for the colormap
vmin = 1
vmax = 1
for year in geotagged_df['map_year'].unique():
    for hist_country in geotagged_df.loc[geotagged_df['map_year'] == year, 'historical_coutry_name' ].unique():
        vmax = max(vmax, geotagged_df.loc[(geotagged_df['map_year'] == year) & (geotagged_df['historical_coutry_name'] == hist_country), 'weight'].sum())
norm = colors.Normalize(vmin=vmin, vmax=vmax)

for idx,y in enumerate(years):
    folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/geojson"

    # Load the GeoJSON map
    geojson_path = folder_path + '/world_' + str(y)+ '.geojson'
    gdf = gpd.read_file(geojson_path)

    # Create a DataFrame from the dictionary
    data_df = pd.DataFrame(list(plot_dict_dicts[y].items()), columns=['country', 'weight'])
    data_df.set_index('country', inplace=True)
    
    gdf['weight'] = 0

    gdf = gdf.set_index('NAME')

    # Define the colormap for non-zero values
    cmap = plt.cm.OrRd

    # Create a new 'color' column in the GeoDataFrame and set it to white (neutral) for all countries
    gdf['color'] = 'white'

    # Set the color for countries with available data
    for country, weight in plot_dict_dicts[y].items():
        if weight > 0:
            color_rgb = cmap(norm(weight))[:3]  # Get RGB values from the colormap
            gdf.loc[gdf.index == country, 'color'] = '#%02x%02x%02x' % tuple(int(c * 255) for c in color_rgb)

    # Plotting the choropleth map
    fig, ax = plt.subplots(1, 1,  figsize=(15, 10))

    # Timer
    timer = fig.canvas.new_timer(interval = 3000) #creating a timer object and setting an interval of 3000 milliseconds
    timer.add_callback(close_event)

    ax.set_aspect('equal')  
    gdf.plot(facecolor=gdf['color'], edgecolor='0.8', linewidth=0.8, ax=ax, legend=True)

    # Write years in title 
    if idx < len(years)-1:
        ax.set_title('Choropleth Map {} - {}'.format(str(y), years[idx+1]))
    else:
        ax.set_title('Choropleth Map {} - {}'.format(str(y), 'now'))
    ax.set_axis_off()  # Turn off the axis to remove the axis frame
    plt.savefig('plots/'+ax.get_title() + '.png')
    timer.start()
    plt.show()
    