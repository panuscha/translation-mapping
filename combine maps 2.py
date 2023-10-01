import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.ops import cascaded_union


# Load the first GeoJSON file (source file with the two polygons to select)
source_gdf = gpd.read_file('historical-basemaps/geojson/world_1960.geojson')





#### EAST AND WEST GERMANY #####

# Load the second GeoJSON file (target file where you want to replace one polygon)
target_gdf = gpd.read_file('historical-basemaps/geojson/world_2010.geojson')

# Select the two polygons from the source file
                                    # East and West Germany
east_and_west_germany = source_gdf.iloc[143:145]

# Replace one polygon in the target file with the selected polygons
# For example, replace the first polygon in the target file with the selected polygons
not_germany = target_gdf[target_gdf.NAME != "Germany"]
combined_gdf = gpd.GeoDataFrame(pd.concat([ not_germany , east_and_west_germany], ignore_index=True))




##### BELGIUM #####

# Load GeoJSON file with NUTS 1
gdf1 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/language-basemaps/NUTS_lvl_1.geojson')

# Define area that is not Belgium 
not_belgium = combined_gdf[combined_gdf.NAME != "Belgium"]

# Get french speaking part of Belgium
belgium_fre = gdf1[gdf1['NUTS_ID'].isin(['BE3'])]

# Get flemish speaking part of Belgium 
belgium_dut = gdf1[gdf1['NUTS_ID'].isin(['BE1', 'BE2'])]
# Combine to one geometry
belgium_dut_geometry = belgium_dut.unary_union
# Create GeoDataFrame
belgium_dut_gdf = gpd.GeoDataFrame(geometry=[belgium_dut_geometry])
belgium_dut_gdf['NAME'] = 'Belgium dut'

# Combine the rest of the world and flemish and french part of Belgium into one GeoDataFrame 
combined_gdf = gpd.GeoDataFrame(pd.concat([ not_belgium , belgium_dut_gdf, belgium_fre ], ignore_index=True))
# Name
combined_gdf.loc[combined_gdf.NUTS_ID == 'BE3','NAME'] = 'Belgium fre'
combined_gdf.iloc[240]['NAME'] = 'Belgium dut'




##### SPAIN ######

# Define area that is not Spain 
not_spain = combined_gdf[combined_gdf.NAME != "Spain"]

# Get spanish speaking part of the world
spain_esp = gdf1[gdf1['NUTS_ID'].isin(['ES1', 'ES2', 'ES3', 'ES4', 'ES6', 'ES7'])]
# Combine into one geometry
spain_esp_geometry = spain_esp.unary_union
# Create GeoDataFrame
spain_esp_gdf = gpd.GeoDataFrame(geometry=[spain_esp_geometry])
spain_esp_gdf['NAME'] = 'Spain'

# Get catalonian speaking part of the world
spain_cat = gdf1[gdf1['NUTS_ID'].isin(['ES5'])]

# Combine the rest of the world and spanish and catalonian part of Spain into one GeoDataFrame 
combined_gdf = gpd.GeoDataFrame(pd.concat([ not_spain, spain_esp_gdf, spain_cat ], ignore_index=True))
combined_gdf.loc[combined_gdf.NUTS_ID == 'ES5','NAME'] = 'Catalonia'



##### SWITZERLAND ####

gdf1 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/language-basemaps/NUTS_lvl_2.geojson')

#switzerland_nuts = gdf1[gdf1['NUTS_ID'].str.startswith('CH')]
not_switzerland = combined_gdf[combined_gdf.NAME != "Switzerland"]

## French swiss
switzerland_fre = gdf1[gdf1['NUTS_ID'].isin(['CH01', 'CH02'])]
switzerland_fre_geometry = switzerland_fre.unary_union
switzerland_fre_gdf = gpd.GeoDataFrame(geometry=[switzerland_fre_geometry])
switzerland_fre_gdf['NAME'] = 'Switzerland fre'

## German swiss
switzerland_ger = gdf1[gdf1['NUTS_ID'].isin(['CH03', 'CH04', 'CH05', 'CH06'])]
switzerland_ger_geometry = switzerland_ger.unary_union
switzerland_ger_gdf = gpd.GeoDataFrame(geometry=[switzerland_ger_geometry])
switzerland_ger_gdf['NAME'] = 'Switzerland ger'

##Italian swiss
switzerland_it = gdf1[gdf1['NUTS_ID'].isin(['CH07'])]
 
combined_gdf = gpd.GeoDataFrame(pd.concat([ not_switzerland , switzerland_fre_gdf, switzerland_ger_gdf, switzerland_it], ignore_index=True))
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH07','NAME'] = 'Switzerland ita'


# Add more GeoDataFrames as needed
combined_gdf.to_file('language-basemaps/combined.geojson', driver='GeoJSON')

fig, ax = plt.subplots(figsize=(10, 8))
combined_gdf.plot(ax=ax, color = None, edgecolor = 'black', linewidth=1)

# Show the plot
plt.show()