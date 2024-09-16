import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.ops import unary_union

year = 2011
gdf = gpd.read_file(f'historical-basemaps/years/world_{year}.geojson')

# All indices
all_indices = gdf.index


# Row position of islands in map from 2011 
GB1 = slice(191, 210)
GB2 = 211
in_GB = list(range(*GB1.indices(len(gdf))))
in_GB.append(GB2)
in_GB = pd.Index(in_GB)


SW = [177, 178]

GR = [189]

DK = [210]

IT = [144]

plot = True
plot_country = 'Denmark'

for year in [1918, 1929, 1945, 1956, 1967, 1978, 1989, 2000, 2011]: #

    # Load the first GeoJSON file (source file with the two polygons to select)
    source_gdf = gpd.read_file(f'historical-basemaps/temp/world_{year}.geojson')

    ###### GB ######

    not_gb = source_gdf[~source_gdf.NAME.isin(['United Kingdom'])] 
    gb = gdf[gdf.NAME.isin(['United Kingdom']) | gdf.index.isin(in_GB)]

    # Combine into one geometry
    gb_geometry = gb.unary_union
    # Create GeoDataFrame
    gb_gdf = gpd.GeoDataFrame(geometry=[gb_geometry])
    gb_gdf['NAME'] = 'United Kingdom'

    combined_gdf = gpd.GeoDataFrame(pd.concat([ not_gb, gb_gdf], ignore_index=True))

    if year < 1945: 
        not_gb_ir = combined_gdf[~combined_gdf.NAME.isin(['United Kingdom of Great Britain and Ireland'])] 
        ireland = gdf[gdf.NAME.isin(['Ireland'])] 

        combined_gdf = gpd.GeoDataFrame(pd.concat([ not_gb_ir, ireland], ignore_index=True))

    ###### SWEDEN ######

    not_sweden = combined_gdf[~combined_gdf.NAME.isin(['Sweden'])] 
    sweden = gdf[gdf.NAME.isin(['Sweden']) | gdf.index.isin(SW)]

    # Combine into one geometry
    sweden_geometry = sweden.unary_union
    # Create GeoDataFrame
    sweden_gdf = gpd.GeoDataFrame(geometry=[sweden_geometry])
    sweden_gdf['NAME'] = 'Sweden'

    combined_gdf = gpd.GeoDataFrame(pd.concat([ not_sweden, sweden_gdf], ignore_index=True))



    if year < 1945: 
        ##### USSR ####
        not_ussr = combined_gdf[~combined_gdf.NAME.isin(["USSR", 'Ukraine', 'White Russia']) ]

        # USSR 
        USSR = combined_gdf[combined_gdf.NAME.isin(["USSR", 'Ukraine', 'White Russia'])]
        # Combine into one geometry
        ussr_geometry = USSR.unary_union
        # Create GeoDataFrame
        ussr_gdf = gpd.GeoDataFrame(geometry=[ussr_geometry])
        ussr_gdf['NAME'] = 'USSR'

        # Combine the rest of the world and spanish and catalonian part of Spain into one GeoDataFrame 
        combined_gdf = gpd.GeoDataFrame(pd.concat([ not_ussr, ussr_gdf], ignore_index=True))



        ##### KALININGRAD #####

        gdf1 = gpd.read_file(f'historical-basemaps/years/world_1918.geojson')

        ## not Germany
        not_germany =  combined_gdf[~combined_gdf.NAME.isin(['East Prussia', 'Germany'])]

        # Germany
        Germany = gdf1[gdf1.NAME.isin(['East Prussia', 'Germany'])]
        # Combine into one geometry
        germany_geometry = Germany.unary_union
        # Create GeoDataFrame
        germany_gdf = gpd.GeoDataFrame(geometry=[germany_geometry])
        germany_gdf['NAME'] = 'Germany'

        # Combine the rest of the world and spanish and catalonian part of Spain into one GeoDataFrame 
        combined_gdf = gpd.GeoDataFrame(pd.concat([ not_germany, germany_gdf], ignore_index=True))

        # Add more GeoDataFrames as needed
        combined_gdf.to_file(f'historical-basemaps/temp/world_{year}.geojson', driver='GeoJSON')


    ###### RHODOS ##### 

    if year > 1929: 

        not_greece = combined_gdf[~combined_gdf.NAME.isin(['Greece'])] 
        greece =  gdf[gdf.NAME.isin(['Greece']) | gdf.index.isin(GR)]

        # Combine into one geometry
        greece_geometry = greece.unary_union
        # Create GeoDataFrame
        greece_gdf = gpd.GeoDataFrame(geometry=[greece_geometry])
        greece_gdf['NAME'] = 'Greece'

        combined_gdf = gpd.GeoDataFrame(pd.concat([ not_greece, greece_gdf], ignore_index=True))

    else: 

        ### FROM WIKI: Trieste - Assigned to Italy from Austria-Hungary after World War I, at the end of World War II it was part of the Zone B of the Free Territory of Trieste, controlled by Yugoslavia.
        
        # Load the first GeoJSON file (source file with the two polygons to select)
        italy_gdf = gpd.read_file(f'historical-basemaps/temp/world_Italy.geojson')
        not_italy = combined_gdf[~combined_gdf.NAME.isin(['Italy'])] 
        italy = italy_gdf[italy_gdf.index.isin(IT) ]

        #print(italy_gdf[italy_gdf.NAME.isin(['Italy'])].geometry)

        rhodos = gdf[gdf.index.isin(GR)]

        italy = pd.concat([italy, rhodos])

        # Combine into one geometry
        italy_geometry = italy.unary_union
        # Create GeoDataFrame
        italy_gdf = gpd.GeoDataFrame(geometry=[italy_geometry])
        italy_gdf['NAME'] = 'Italy'

        combined_gdf = gpd.GeoDataFrame(pd.concat([ not_italy, italy_gdf], ignore_index=True))


    ###### TURKEY ##### 

    if year < 1945: 

        not_turkey = combined_gdf[~combined_gdf.NAME.isin(['Turkey'])] 
        turkey =  gdf[gdf.NAME.isin(['Turkey'])]

        combined_gdf = gpd.GeoDataFrame(pd.concat([ not_turkey, turkey], ignore_index=True))


    ###### DENMARK ######

    denmark_gdf = gpd.read_file(f'historical-basemaps/temp/world_Denmark.geojson')

    not_denmark = combined_gdf[~combined_gdf.NAME.isin(['Denmark'])] 
    denmark = denmark_gdf[denmark_gdf.NAME.isin(['Denmark'])]
    faroe = gdf[gdf.index.isin(DK)]

    denmark = pd.concat([denmark, faroe])

    # Combine into one geometry
    denmark_geometry = denmark.unary_union
    # Create GeoDataFrame
    denmark_gdf = gpd.GeoDataFrame(geometry=[denmark_geometry])
    denmark_gdf['NAME'] = 'Denmark'

    combined_gdf = gpd.GeoDataFrame(pd.concat([ not_denmark, denmark_gdf], ignore_index=True))



    ####### SPAIN #####

    not_spain = combined_gdf[~combined_gdf.NAME.isin(['Spain'])] 
    spain = gdf[gdf.NAME.isin(['Spain'])]

    combined_gdf = gpd.GeoDataFrame(pd.concat([ not_spain, spain], ignore_index=True))


    combined_gdf.to_file(f'historical-basemaps/temp/world_{year}.geojson', driver='GeoJSON')


    if plot: 
        # Create a plot
        fig, ax = plt.subplots()

        # Plot polygons with NAME != None (in default color)
        combined_gdf.plot(ax=ax, color='lightgray', edgecolor='black')

        # Plot polygons with NAME == None (in red color)
        combined_gdf[combined_gdf.NAME == plot_country].plot(ax=ax, color='red', edgecolor='black')

        # Customize and show the plot
        plt.title(f'{plot_country} {year}')
        plt.show()
