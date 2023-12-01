import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the GeoJSON files
gdf2 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/geojson/world_1960.geojson')

# Define a list of specific "NUTS_ID" values to remove
values_to_remove = ['Luxembourg', 'Switzerland', 'France', 'France', 'Ireland', 'United Kingdom', 'Belgium', 'Hungary', 'Romania', 'Bulgaria', 'Spain', 'Greece', 'Denmark', 'Poland', 'Netherlands', 'Austria', 'Finland', 'Sweden', 'Czechoslovakia', 'East Germany', 'West Germany', 'Italy', 'Yugoslavia', 'Italy', 'Iceland', 'Turkey']

# Filter the GeoDataFrame to exclude polygons with "NUTS_ID" in the list
gdf2_filtered = gdf2[~gdf2['NAME'].isin(values_to_remove)]

gdf1 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/language-basemaps/NUTS_lvl_1.geojson')
print([x for x in gdf1.NUTS_ID])

combined = [gdf1]

# Combine countries


for i in ['AT', 'FR', 'FI', 'HU', 'PL' , 'UK', 'ES', 'IT', 'TR', 'SE', 'RO', 'PT', 'NL', 'HU', 'EL', 'BG', ['DE4', 'DE8', 'DED', 'DEE',  'DEG'], ['DE1', 'DE2', 'DE3', 'DE5', 'DE6', 'DE7', 'DE9','DEA', 'DEB', 'DEC', 'DEF']]:
    
    if isinstance(i, list):
        selected_polygons = gdf1[gdf1['NUTS_ID'].isin(i)]

    else:    
        # Filter polygons based on criteria (e.g., attribute value)
        selected_polygons = gdf1[gdf1['NUTS_ID'].str.startswith(i)]

    combined_geometry = selected_polygons.unary_union

    # Create a new GeoDataFrame with the combined geometry
    combined_gdf = gpd.GeoDataFrame(geometry=[combined_geometry])

    combined.append(combined_gdf)


# Create a new GeoDataFrame with the combined geometry
combined_gdf = gpd.GeoDataFrame(geometry=[combined_geometry])

combined.append(combined_gdf)






gdf1= gpd.GeoDataFrame(pd.concat(combined, ignore_index=True))

# Load more GeoJSON files as needed
combined_gdf = gpd.GeoDataFrame(pd.concat([gdf2_filtered, gdf1], ignore_index=True))
# Add more GeoDataFrames as needed
combined_gdf.to_file('combined.geojson', driver='GeoJSON')

fig, ax = plt.subplots(figsize=(10, 8))
combined_gdf.plot(ax=ax, color = None, edgecolor='black', linewidth=1)

# Show the plot
plt.show()