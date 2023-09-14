import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the GeoJSON files
gdf2 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/historical-basemaps/geojson/world_1960.geojson')
gdf1 = gpd.read_file('C:/Users/Panuskova/Nextcloud/translation-mapping/language-basemaps/NUTS_lvl_1.geojson')
print([x for x in gdf1.NUTS_ID])

combined = [gdf1]

for i in ['AT', 'FR', 'FI', 'HU', 'PL' , 'UK', 'ES', 'IT', 'TR']:
    # Filter polygons based on criteria (e.g., attribute value)
    selected_polygons = gdf1[gdf1['NUTS_ID'].str.startswith(i)]

    combined_geometry = selected_polygons.unary_union

    # Create a new GeoDataFrame with the combined geometry
    combined_gdf = gpd.GeoDataFrame(geometry=[combined_geometry])

    combined.append(combined_gdf)

gdf1= gpd.GeoDataFrame(pd.concat(combined, ignore_index=True))

# Load more GeoJSON files as needed
combined_gdf = gpd.GeoDataFrame(pd.concat([gdf2, gdf1], ignore_index=True))
# Add more GeoDataFrames as needed
combined_gdf.to_file('combined.geojson', driver='GeoJSON')

fig, ax = plt.subplots(figsize=(10, 8))
combined_gdf.plot(ax=ax, color = None, edgecolor='black', linewidth=1)

# Show the plot
plt.show()