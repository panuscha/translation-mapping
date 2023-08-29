import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd


folder_path = "C:/Users/Panuskova/Nextcloud/translation-mapping/"

geotagged_df = pd.read_csv("geotagged/geotagged_lang.csv")


 

# Load the GeoJSON map
historical_geojson_path = folder_path + 'historical-basemaps/geojson/world_' + str(1960)+ '.geojson'

# Read historical borders GeoJSON using GeoPandas
historical_borders = gpd.read_file(historical_geojson_path)

language_geojson_path = folder_path + 'language-basemaps/' + "GERMAN SPEAKING.geojson"

# Read coloring GeoJSON using GeoPandas
coloring_data = gpd.read_file(language_geojson_path)

# Create a base plot
fig, ax = plt.subplots(figsize=(10, 8))
coloring_data.plot(ax=ax, color='red', edgecolor='none', linewidth=1)
historical_borders.plot(ax=ax, color='none', edgecolor='black', linewidth=0.5)



# Customize plot appearance
ax.set_title('Historical Map')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Show the plot
plt.show()
