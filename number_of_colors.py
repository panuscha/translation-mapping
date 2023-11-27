import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolor

LIMIT = 0.02
TOP = 3
MIN_TRANS = 4



# Table with number of translations for each country, language and decade
df = pd.read_excel("D:\\Panuskova\\Nextcloud\\translation-mapping\\translation-mapping\\weights\\translations_language_countries.xlsx")

# all plot years
plot_years = df.map_year.unique()#['1918', '1929', '1945', '1956', '1967','1978', '1989', '2000', '2011' ] 

# all countries and languages
countries = list(df.country.unique())#["Finland", "Ukraine", "Italy", "Lithuania" ,"Yugoslavia",  "Germany (USA)",  "Denmark",  "Austria", "Portugal", "Belgium",  "Czechoslovakia", "Byelarus", "United Kingdom", "Iceland", "Poland", "Germany", "Albania", "Romania","Ireland", "Slovakia", "Netherlands", "Latvia", "Switzerland",  "Hungary", "Sweden" , "USSR",  "Greece", "Spain", "France", "Bosnia and Herzegovina", "Norway", "West Germany"] 
countries.remove('Czech Republic')
countries.remove('Japan')
#df.country.unique() 
languages = df.language.unique()

needed_languages = set()
needed_countries = set()

for plot_year in plot_years:
    
    # Iterate through countries to plot the bar chart                
    for country in countries:
        
        # Select only non empty rows that are in the decade and for that country
        if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:

            # All non-empty rows
            h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
            
            # if only weights, change to h.weights
            sum_weights = sum(h.weights)
            
            weights_max = max(h.weights)
            
            if (sum_weights-weights_max)/sum_weights >= LIMIT:
                
                # Discard the most common language (= should be the major language)
                h = h[h.weights != weights_max]
                
                max_id = min([len(h), TOP])
                
                try:
                    for i in range(max_id):
                        weights_max = max(h.weights)
                        if weights_max > MIN_TRANS :
                            id = h.index[h.weights == weights_max]
                            needed_languages.add(h.language[id[0]])
                            needed_countries.add(country)
                            h = h[h.weights != weights_max]
                except:
                    print(country + str(plot_year))
                        
                    
print("Limit: " + str(LIMIT))         
print("Countries: " + str(len(needed_countries))) 
print(' '.join(needed_countries))
print("Languages: " + str(len(needed_languages)))            
print(' '.join(needed_languages))                

                
            
            