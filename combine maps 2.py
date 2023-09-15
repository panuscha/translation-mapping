import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# Load the first GeoJSON file (source file with the two polygons to select)
source_gdf = gpd.read_file('historical-basemaps/geojson/world_1960.geojson')

# Load the second GeoJSON file (target file where you want to replace one polygon)
target_gdf = gpd.read_file('historical-basemaps/geojson/world_2010.geojson')

# Select the two polygons from the source file
                                    # East and West Germany
selected_polygons = source_gdf.iloc[143:145]
east_and_west_germany = source_gdf.iloc[143:145]

# Replace one polygon in the target file with the selected polygons
# For example, replace the first polygon in the target file with the selected polygons
not_germany = target_gdf[target_gdf.NAME != "Germany"]
combined_gdf = gpd.GeoDataFrame(pd.concat([ not_germany , east_and_west_germany], ignore_index=True))


# Save the modified target file as a new GeoJSON file
#target_gdf.to_file('modified_target.geojson', driver='GeoJSON')


fig, ax = plt.subplots(figsize=(10, 8))
combined_gdf.plot(ax=ax, color = None, edgecolor = 'black', linewidth=1)

# Show the plot
plt.show()