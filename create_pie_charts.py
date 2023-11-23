import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# all plot years
plot_years = ['1918', '1929', '1945', '1956', '1967','1978', '1989', '2000', '2011' ] 

# Table with number of translations for each country, language and decade
df = pd.read_excel("D:\\Panuskova\\Nextcloud\\translation-mapping\\translation-mapping\\weights\\translations_language_countries.xlsx")

# all countries and languages
countries = df.country.unique()
languages = df.language.unique()

my_color_palette = {}
all_colors = list(mcolors.CSS4_COLORS.keys())

# Save color for each country
for i, language in enumerate(languages):
    my_color_palette[language] = all_colors[i]

# Iterate through all decades
for plot_year in plot_years: 

    # Iterate through countries to plot the bar chart                
    for country in countries:

        # Select only non empty rows that are in the decade and for that country
        if not df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)].empty:

            # All non-empty rows
            h = df[(df['map_year'] == int(plot_year)) &  (df['country'] == country)]
            
            # if only weights, change to h.weights
            sum_weights = sum(h.weights)
            
            size = 0.1
        
            h_max = max(h.weights)
            
            id = h.index[h.weights == h_max]
            
            outer_colors = [my_color_palette[h.language[id[0]]] , 'black' ]

            weights_all = [h_max, sum(h.weights) - h_max ]
            
            fig, ax = plt.subplots()
            n = ax.pie(weights_all, radius=1, colors=outer_colors,
            wedgeprops=dict(width=size, edgecolor='w'))
            n[0][0].set_alpha(0.0)

            # Discard the most common language (= should be the major language)
            h = h[h.weights != h_max]

            if not(h.empty):

                # get all colors for languages 
                inner_colors = [my_color_palette[language] for language in h.language  ]

                # get all languages 
                language = h.language
                
                # if only weights, change to h.weights
                weights = [w/sum_weights for w in h.weights] 

                ax.pie(weights, radius=1-size, colors=inner_colors,
                wedgeprops=dict(edgecolor='w')) #width=size, 

                plt.title("{country}_{year}".format(country = country, year = plot_year))
                plt.show()
                #hist = h[['language','weights']].plot(kind = 'bar', figsize=(8, 6), x = 'language', ylim = [0, y_max], color = colors).get_figure()
                plt.savefig('D:\\Panuskova\\Nextcloud\\translation-mapping\\translation-mapping\\plots\\histograms minor percentage pie charts\\{country}_{year}'.format(country = country, year = plot_year))
                plt.close()
                #close(hist)
      
