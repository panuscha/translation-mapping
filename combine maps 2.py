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
gdf1 = gpd.read_file('language-basemaps/NUTS_lvl_1.geojson')

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

# Get spanish speaking part of Spain
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

gdf1 = gpd.read_file('language-basemaps/NUTS_lvl_2.geojson')

#switzerland_nuts = gdf1[gdf1['NUTS_ID'].str.startswith('CH')]
not_switzerland = combined_gdf[combined_gdf.NAME != "Switzerland"]

not_switzerland = not_switzerland[not_switzerland.NAME != '' ] 

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
combined_gdf = gpd.GeoDataFrame(pd.concat([ not_switzerland , switzerland_fre_gdf, switzerland_ger_gdf, switzerland_it ], ignore_index=True))
combined_gdf.loc[combined_gdf.NUTS_ID == 'CH07','NAME'] = 'Switzerland ita'

combined_gdf = combined_gdf[combined_gdf['NAME'].notna()]


##### CANADA ####

gdf1 = gpd.read_file('language-basemaps/US CANADA NUTS.geojson')

not_canada = combined_gdf[combined_gdf.NAME != "Canada"]

## English Canada
canada_eng = gdf1[(gdf1["CNTRY"] == "Canada") & (gdf1["name"] != "Quebec")]
canada_eng_geometry = canada_eng.unary_union
canada_eng_gdf = gpd.GeoDataFrame(geometry=[canada_eng_geometry])
canada_eng_gdf['NAME'] = 'Canada eng'

## French Canada
canada_fre = gdf1[gdf1["name"] == "Quebec"]
combined_gdf = gpd.GeoDataFrame(pd.concat([ not_canada, canada_eng_gdf, canada_fre ], ignore_index=True))
combined_gdf.loc[combined_gdf.name == "Quebec",'NAME'] = 'Canada fre'

# Add more GeoDataFrames as needed
combined_gdf.to_file('language-basemaps/combined.geojson', driver='GeoJSON')

fig, ax = plt.subplots(figsize=(10, 8))
combined_gdf.plot(ax=ax, color = None, edgecolor = 'black', linewidth=1)

# Show the plot
plt.show()

['Luxembourg', 'Korea, Republic of', 'Cyprus', 'Japan', 'Bhutan', 'Western Sahara', 'Qatar', 'United Arab Emirates', 'Taiwan', 'Mali', 'Oman', 'Niger', 'Chad', 'Vietnam', 'Cuba', 'Laos', 'United States', 'China', 'Haiti', 'Dominican Republic', 'Philippines', 'Puerto Rico', 'Jamaica', 'Burkina Faso', 'Nicaragua', 'Cambodia', 'Costa Rica', 'Central African Republic', 'Sierra Leone', 'Sri Lanka', 'Panama', 'Guyana', 'Liberia', 'Zaire', 'Tanzania, United Republic of', 'Rwanda', 'Burundi', 'Angola', 'Zambia', 'Malawi', 'Bolivia', 'Mozambique', 'Madagascar', 'Zimbabwe', 'Namibia', 'Chile', 'Botswana', 'Paraguay', 'South Africa', 'Swaziland', 'Lesotho', 'New Zealand', 'Argentina', 'Iceland', 'Estonia', 'Latvia', 'Lithuania', 'Byelarus', 'United Kingdom', 'Kazakhstan', 'Ireland', 'Ukraine', 'Mongolia', 'Slovakia', 'Hungary', 'Moldova', 'Romania', 'Slovenia', 'Croatia', 'Serbia', 'Uzbekistan', 'Bosnia and Herzegovina', 'Bulgaria', 'Georgia', 'Montenegro', 'Kyrgyzstan', "Korea, Democratic People's Republic of", 'Turkmenistan', 'Albania', 'Macedonia', 'Portugal', 'Turkey', 'Azerbaijan', 'Greece', 'Armenia', 'Tajikistan', 'Iran', 'Afghanistan', 'Iraq', 'Syria', 'Tunisia', 'Algeria', 'Morocco', 'Lebanon', 'Mexico', 'Kuwait', 'Burma', 'Bangladesh', 'Thailand', 'Belize', 'Guatemala', 'Honduras', 'El Salvador', 'Colombia', 'Benin', 'Ghana', 'Togo', 'Ivory Coast', 'Malaysia', 'Suriname', 'French Guiana', 'Congo', 'Gabon', 'Equatorial Guinea', 'Ecuador', 'Peru', 'Brazil', 'Papua New Guinea', 'Australia', 'Uruguay', 'Denmark', 'Poland', 'Netherlands', 'Czech Republic', 'Nigeria', 'Cameroon', 'Pakistan', 'India', 'Jordan', 'Libya', 'Israel', 'Saudi Arabia', 'Egypt', 'Nepal', 'Mauritania', 'Sudan', 'Yemen', 'Eritrea', 'Senegal', 'Ethiopia', 'Gambia, The', 'Djibouti', 'Guinea-Bissau', 'Guinea', 'Venezuela', 'Somalia', 'Trinidad', 'Brunei', 'Kenya', 'Uganda', 'Indonesia', 'Greenland', 'Russia', 'Norway', 'Finland', 'Sweden', 'Turkish Cypriot-administered area', 'Russia', 'Antigua and Barbuda', 'Barbados', 'Dominica', 'Grenada', 'Martinique', 'Montserrat', 'Anguilla', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'United States Virgin Islands', 'Guadeloupe', 'Netherlands Antilles', 'Saint Martin', 'Saint Barthelemy', 'Turks and Caicos Islands', 'Bahamas', 'United States', 'United States', 'Austria', 'Liechtenstein', 'Italy', 'Malta', 'Italy', 'France', 'Italy', 'American Samoa', 'Fiji', 'Niue', 'Tonga', 'Wallis and Futuna Islands', 'Samoa', 'Rapa Nui', 'East Germany', 'West Germany', 'Belgium dut', 'Belgium fre', 'Spain', 'Catalonia', 'Switzerland fre', 'Switzerland ger', 'Switzerland ita', 'Canada eng', 'Canada fre']