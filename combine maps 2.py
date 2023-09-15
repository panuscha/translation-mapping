import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

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

gdf1 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/language-basemaps/NUTS_lvl_1.geojson')

belgium_nuts = gdf1[gdf1['NUTS_ID'].isin(['BE1', 'BE2', 'BE3'])]
not_belgium = combined_gdf[combined_gdf.NAME != "Belgium"]

combined_gdf = gpd.GeoDataFrame(pd.concat([ not_belgium , belgium_nuts], ignore_index=True))
combined_gdf.loc[combined_gdf.NUTS_ID == 'BE3','NAME'] = 'Belgium fre'
combined_gdf.loc[combined_gdf.NUTS_ID == 'BE2','NAME'] = 'Belgium dut'
combined_gdf.loc[combined_gdf.NUTS_ID == 'BE1','NAME'] = 'Belgium dut'

# Save the modified target file as a new GeoJSON file
#target_gdf.to_file('modified_target.geojson', driver='GeoJSON')

##### SWITZERLAND ####

gdf1 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/language-basemaps/NUTS_lvl_2.geojson')

switzerland_nuts = gdf1[gdf1['NUTS_ID'].str.startswith('CH')]
not_switzerland = combined_gdf[combined_gdf.NAME != "Switzerland"]

combined_gdf = gpd.GeoDataFrame(pd.concat([ not_switzerland , switzerland_nuts], ignore_index=True))
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH01','NAME'] = 'Switzerland fre'
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH02','NAME'] = 'Switzerland fre'
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH03','NAME'] = 'Switzerland ger'
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH04','NAME'] = 'Switzerland ger'
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH05','NAME'] = 'Switzerland ger'
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH06','NAME'] = 'Switzerland ger'
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH07','NAME'] = 'Switzerland it'

# Add more GeoDataFrames as needed
combined_gdf.to_file('combined.geojson', driver='GeoJSON')

fig, ax = plt.subplots(figsize=(10, 8))
combined_gdf.plot(ax=ax, color = None, edgecolor = 'black', linewidth=1)

# Show the plot
plt.show()