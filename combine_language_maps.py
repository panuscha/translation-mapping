import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.ops import unary_union

source_gdf = gpd.read_file(f'language-basemaps/combined.geojson')
gdf = gpd.read_file(f'historical-basemaps/years/world_2011.geojson')

# Row position of islands in map from 2011 
GB1 = slice(191, 210)
GB2 = 211
in_GB = list(range(*GB1.indices(len(gdf))))
in_GB.append(GB2)
in_GB = pd.Index(in_GB)


SW = [177, 178]

GR = [189]

DK = [210]

###### DENMARK ######

denmark_gdf = gpd.read_file(f'historical-basemaps/temp/world_Denmark.geojson')

not_denmark = source_gdf[~source_gdf.NAME.isin(['Denmark'])] 
denmark = denmark_gdf[denmark_gdf.NAME.isin(['Denmark'])]
faroe = gdf[gdf.index.isin(DK)]

denmark = pd.concat([denmark, faroe])

# Combine into one geometry
denmark_geometry = denmark.unary_union
# Create GeoDataFrame
denmark_gdf = gpd.GeoDataFrame(geometry=[denmark_geometry])
denmark_gdf['NAME'] = 'Denmark'

combined_gdf = gpd.GeoDataFrame(pd.concat([ not_denmark, denmark_gdf], ignore_index=True))

###### GB ######

not_gb = combined_gdf[~combined_gdf.NAME.isin(['United Kingdom'])] 
gb = gdf[gdf.NAME.isin(['United Kingdom']) | gdf.index.isin(in_GB)]

# Combine into one geometry
gb_geometry = gb.unary_union
# Create GeoDataFrame
gb_gdf = gpd.GeoDataFrame(geometry=[gb_geometry])
gb_gdf['NAME'] = 'United Kingdom'

combined_gdf = gpd.GeoDataFrame(pd.concat([ not_gb, gb_gdf], ignore_index=True))

###### SWEDEN ######

not_sweden = combined_gdf[~combined_gdf.NAME.isin(['Sweden'])] 
sweden = gdf[gdf.NAME.isin(['Sweden']) | gdf.index.isin(SW)]

# Combine into one geometry
sweden_geometry = sweden.unary_union
# Create GeoDataFrame
sweden_gdf = gpd.GeoDataFrame(geometry=[sweden_geometry])
sweden_gdf['NAME'] = 'Sweden'

combined_gdf = gpd.GeoDataFrame(pd.concat([ not_sweden, sweden_gdf], ignore_index=True))

###### RHODOS ######

not_greece = combined_gdf[~combined_gdf.NAME.isin(['Greece'])] 
greece =  gdf[gdf.NAME.isin(['Greece']) | gdf.index.isin(GR)]

# Combine into one geometry
greece_geometry = greece.unary_union
# Create GeoDataFrame
greece_gdf = gpd.GeoDataFrame(geometry=[greece_geometry])
greece_gdf['NAME'] = 'Greece'

combined_gdf = gpd.GeoDataFrame(pd.concat([ not_greece, greece_gdf], ignore_index=True))

combined_gdf.to_file(f'historical-basemaps/temp/language_map_combined.geojson', driver='GeoJSON')


fig, ax = plt.subplots(figsize=(10, 8))
combined_gdf.plot(ax=ax, color = None, edgecolor = 'black', linewidth=1)

# Show the plot
plt.show()
